# -*- coding: utf-8 -*-
# Copyright 2004-2015 Tech-Receptives
# Copyright 2015-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.osv import fields, orm


class MedicalDiseaseEvidence(orm.Model):
    _name = 'medical.disease.evidence'
    _description = 'Medical Disease Signs & Symptoms'

    clinical_id = fields.Many2one(
        string='Sign or Symptom',
        comodel_name='medical.pathology',
        required=True,
    )
    evaluation_id = fields.Many2one(
        string='Evaluation',
        comodel_name='medical.patient.evaluation',
        required=True,
        readonly=True,
    )
    sign_or_symptom = fields.Selection(
        selection=[
            ('sign', 'Sign'),
            ('symptom', 'Symptom'),
        ],
        string='Subjective / Objective',
        required=True,
    ),
    comments = fields.Char()
