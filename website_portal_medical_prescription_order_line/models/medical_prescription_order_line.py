# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

import datetime


class MedicalPrescriptionOrderLine(models.Model):
    _inherit = 'medical.prescription.order.line'

    is_expired = fields.Boolean(
        string='Expired?',
        compute='_compute_is_expired',
    )

    @api.multi
    def _compute_is_expired(self):
        now = datetime.datetime.now()
        for record in self:
            stop = fields.Datetime.from_string(record.date_stop_treatment)
            record.is_expired = stop and stop < now
