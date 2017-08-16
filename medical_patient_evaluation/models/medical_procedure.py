# -*- coding: utf-8 -*-
# Copyright 2004-2015 Tech-Receptives
# Copyright 2015-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MedicalProcedure(models.Model):
    _name = 'medical.procedure'
    _description = 'Medical Procedure'

    description = fields.Char(
        string='Long Text',
        translate=True,
    )
    name = fields.char(
        string='Code',
        required=True,
    )
