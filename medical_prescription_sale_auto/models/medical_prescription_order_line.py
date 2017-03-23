# -*- coding: utf-8 -*-
# Copyright 2017 Specialty Medical Drugstore LLC
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models

import logging


_logger = logging.getLogger(__name__)


class MedicalPrescriptionOrderLine(models.Model):
    _inherit = 'medical.prescription.order.line'

    @api.multi
    def write(self, vals, ):
        super(MedicalPrescriptionOrderLine, self).write(vals)
        if self.prescription_order_id.stage_id.is_verified:
            product = self.medical_medication_id.medicament_id.product_id
            sale_order_lines = self.env['sale.order.line'].search(
                [('product_id', '=', product.id)]
            )
            exceptions = []
            if sale_order_lines:
                for line in sale_order_lines:
                    if (line.product_uom_qty == self.quantity and
                            line.product_id ==
                            self.medical_medication_id.
                            medicament_id.product_id and
                            self.patient_id in
                            line.order_partner_id.patient_ids):
                        line.write({'state': 'confirmed'})
                    else:
                        line.write({'state': 'exception'})
                        exceptions += line
            else:
                self.env['crm.lead'].create({
                    'name': 'Prescription for %s' % product.name,
                    'partner_id': self.prescription_order_id.partner_id.id,
                })
            if exceptions:
                for e in exceptions:
                    self.env['ir.cron'].create({
                        'name': 'Split exception into own order',
                        'numbercall': -1,
                        'interval_number': 10,
                        'interval_type': 'minutes',
                        'model': 'sale.order.line',
                        'function': '_split_order_line_exceptions',
                    })
            elif sale_order_lines:
                for line in sale_order_lines:
                    sale_order = line.order_id
                    if sale_order.state != 'confirmed':
                        sale_order.write({'state': 'confirmed'})
