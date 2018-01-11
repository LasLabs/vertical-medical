# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from itertools import groupby
from odoo import _, api, fields, models


class MedicalPrescriptionOrderLine(models.Model):
    _inherit = 'medical.prescription.order.line'

    sale_crm_auto_ran = fields.Boolean()

    @api.multi
    def write(self, vals):
        verified_recs = self.filtered(lambda r: r.stage_id.is_verified)

        super_result = super(MedicalPrescriptionOrderLine, self).write(vals)

        verified_recs_now = self.filtered(lambda r: r.stage_id.is_verified)
        new_verified_recs = verified_recs_now - verified_recs
        new_verified_recs._sale_crm_auto()

        return super_result

    @api.multi
    def _sale_crm_auto(self):
        need_leads = []

        for record in self:
            if record.sale_crm_auto_ran:
                continue

            for sale_line in record.sale_order_line_ids:
                if record._sale_line_matches(sale_line):
                    sale_line.sale_crm_auto_state = 'confirmed'
                else:
                    sale_line.sale_crm_auto_state = 'exception'

            if not record.sale_order_line_ids:
                need_leads += record

            for sale_order in record.sale_order_ids:
                unconfirmed_lines = sale_order.order_line.filtered(
                    lambda r: r.sale_crm_auto_state != 'confirmed'
                )
                locked = sale_order.state in ('sale', 'done', 'cancel')
                if not unconfirmed_lines and not locked:
                    sale_order.action_confirm()

            record.sale_crm_auto_ran = True

        def _get_commerce_partner_id(rx_line):
            return rx_line.patient_id.commercial_partner_id.id

        need_leads = sorted(need_leads, key=_get_commerce_partner_id)
        for partner_id, group in groupby(need_leads, _get_commerce_partner_id):
            group_ids = [record.id for record in group]
            lead_model = self.env['crm.lead']
            matching_lead = lead_model.search([
                ('partner_id', '=', partner_id),
                ('prescription_order_line_ids', '!=', False),
                ('type', '=', 'opportunity'),
                ('stage_id', '=', lead_model._default_stage_id()),
            ], limit=1)

            if matching_lead:
                lead_line_ids = matching_lead.prescription_order_line_ids.ids
                group_ids += lead_line_ids
                matching_lead.prescription_order_line_ids = [(6, 0, group_ids)]
                self.env['mail.message'].create({
                    'body': _('This opportunity has been expanded to include'
                              'new prescription order lines.'),
                    'model': 'crm.lead',
                    'res_id': matching_lead.id,
                    'message_type': 'notification',
                })
            else:
                lead_model.create({
                    'name': _('Unfilled prescription order lines'),
                    'partner_id': partner_id,
                    'prescription_order_line_ids': [(6, 0, group_ids)],
                    'type': 'opportunity',
                })

    @api.multi
    def _sale_line_matches(self, sale_line):
        self.ensure_one()

        sale_line_partner = sale_line.order_partner_id.commercial_partner_id
        if (sale_line_partner != self.patient_id.commercial_partner_id
                or sale_line.product_id != self.medicament_id.product_id
                or sale_line.product_uom_qty > self.can_dispense_qty):
            return False

        return True
