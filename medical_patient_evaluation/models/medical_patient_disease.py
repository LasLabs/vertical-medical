# -*- coding: utf-8 -*-
# Copyright 2004-2015 Tech-Receptives
# Copyright 2015-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MedicalPatientDisease(models.Model):
    _name = 'medical.patient.disease'
    _description = 'Medical Patient Disease'

    procedure_id = fields.Many2one(
        string='Procedure',
        comodel_name='medical.procedure',
        index=True,
    )
