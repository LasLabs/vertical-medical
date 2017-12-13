# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MedicalPrescriptionOrderLine(models.Model):
    _inherit = 'medical.prescription.order.line'

    verify_method = fields.Selection(
        related='prescription_order_id.verify_method',
    )

    @api.multi
    def write(self, vals):
        """Overload to limit state changes for verified lines"""
        STATE_MODULE = 'medical_prescription_state'
        exception_state = self.env.ref(
            STATE_MODULE + '.prescription_order_line_state_exception'
        )

        verified_recs = self.filtered(lambda r: r.stage_id.is_verified)
        if verified_recs and 'stage_id' in vals:
            stage_model = self.env['base.kanban.stage']
            stage = stage_model.search([('id', '=', vals['stage_id'])])
            if stage != exception_state and not stage.is_verified:
                raise ValidationError(
                    _('You are trying to move one or more verified Rx lines to'
                      ' a disallowed unverified state (e.g. %s). Please mark'
                      ' them as exceptions if manual changes are required.')
                    % verified_recs[0].name
                )

        return super(MedicalPrescriptionOrderLine, self).write(vals)
