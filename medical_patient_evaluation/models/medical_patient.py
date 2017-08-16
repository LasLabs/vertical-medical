# -*- coding: utf-8 -*-
# Copyright 2004-2015 Tech-Receptives
# Copyright 2015-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MedicalPatient(models.Model):
    _inherit = 'medical.patient'

    @api.one
    def action_invalidate(self):
        super(MedicalPatient, self).action_invalidate()
        self.disease_ids.action_invalidate()

    family_id = fields.Many2one(
        comodel_name='medical.family', string='Family')
    blood_type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'), ])
    rh = fields.Selection([
        ('+', '+'),
        ('-', '-')])
    primary_care_physician_id = fields.Many2one(
        comodel_name='medical.physician', string='Primary Care Doctor',
        index=True)
    childbearing_age = fields.Boolean()
    medication_ids = fields.One2many(
        comodel_name='medical.patient.medication', inverse_name='patient_id',
        string='Medications')
    evaluation_ids = fields.One2many(
        comodel_name='medical.patient.evaluation', inverse_name='patient_id',
        string='Evaluations')
    critical_info = fields.Text(
        help='Important diseases, allergies or procedures information',
        string='Critical Information')
    disease_ids = fields.One2many(
        comodel_name='medical.patient.disease', inverse_name='patient_id',
        string='Diseases')
    ethnicity_id = fields.Many2one(
        comodel_name='medical.ethnicity', string='Ethnicity', index=True)
    cause_of_death_pathology_id = fields.Many2one(
        comodel_name='medical.pathology', string='Cause of Death Pathology',
        index=True)
