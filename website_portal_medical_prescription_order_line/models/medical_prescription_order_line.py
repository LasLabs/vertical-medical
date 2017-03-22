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

    @api.one
    def _compute_is_expired(self):
        stop = self.date_stop_treatment
        if stop and type(stop) is str:
            stop = datetime.datetime.strptime(
                stop, "%Y-%m-%d %H:%M:%S"
            )
        for record in self:
            if stop and stop < datetime.datetime.now():
                record.is_expired = True
            else:
                record.is_expired = False
