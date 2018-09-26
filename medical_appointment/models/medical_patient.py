# -*- coding: utf-8 -*-
# Copyright 2017 Mauro Estrella
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class MedicalPatient(models.Model):
    _inherit = 'medical.patient'
    

    appointment_ids = fields.One2many(
        string='Appointments',
        comodel_name='medical.appointment',
        inverse_name='patient_id',
    )
    count_appointment_ids = fields.Integer(
        compute='_compute_count_appointment_ids',
        string='Appointments',
    )
    @api.multi
    def _compute_count_appointment_ids(self):
        for rec_id in self:
            rec_id.count_appointment_ids = len(rec_id.appointment_ids)        
