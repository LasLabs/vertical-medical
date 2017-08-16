# -*- coding: utf-8 -*-
# Copyright 2004-2015 Tech-Receptives
# Copyright 2015-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MedicalProcedureDirections(models.Model):
    _name = 'medical.procedure.directions'

    procedure_id = fields.Many2one(
        string='Procedure',
        comodel_name='medical.procedure',
        required=True,
    )
    evaluation_id = fields.Many2one(
        string='Evaluation',
        comodel_name='medical.patient.evaluation',
        readonly=True,
    )
    comments = fields.Char()
