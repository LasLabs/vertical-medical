# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class MedicalPrescriptionOrderLine(models.Model):
    """
    Add State verification functionality to MedicalPrescriptionOrderLine

    This model disallows editing of a `medical.prescription.order.line` if its
    `prescription_order_id` is in a `verified` state.
    """

    _inherit = 'medical.prescription.order.line'
    _name = 'medical.prescription.order.line'

    @api.multi
    def write(self, vals, ):
        """
        Overload write & perform audit validations

        Raises:
            ValidationError: When a write is not allowed due to being in a
                protected state
        """
        if self.prescription_order_id.stage_id.is_verified:
            raise ValidationError(_(
                'You cannot edit this value after its parent Rx has'
                ' been verified. Please either cancel it, or mark it as'
                ' an exception if manual reversals are required. [%s]' %
                self.prescription_order_id.name
            ))

        return super(MedicalPrescriptionOrderLine, self).write(vals)
