# -*- coding: utf-8 -*-
# Copyright 2004-2015 Tech-Receptives
# Copyright 2015-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MedicalPatientCondition(models.Model):
    _name = 'medical.patient.condition'
    _description = 'Medical Patient Condition',

    evaluation_id = fields.Many2one(
        string='Evaluation',
        comodel_name='medical.patient.evaluation',
        required=True,
        readonly=True,
    )
    pathology_id = fields.Many2one(
        string='Pathology',
        comodel_name='medical.pathology',
    )
    complaint = fields.Text(
        string='Complaint details',
    )
    comments = fields.Char()
