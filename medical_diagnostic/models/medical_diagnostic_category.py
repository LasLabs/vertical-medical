# -*- coding: utf-8 -*-
# Copyright 2012-2013 Federico Manuel Echeverri Choux
# Copyright 2016-2018 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class MedicalDiagnosticCategory(models.Model):
    _name = 'medical.diagnostic.category'
    _description = 'Medical Diagnostic Category'
    _sql_constraints = [
        ('code_uniq', 'UNIQUE(code)', 'Categories must have a unique code!'),
    ]

    code = fields.Char(
        help='Short code for category',
        required=True,
    )
    name = fields.Char(
        help='Name of category, such as "CAT Scan", "Radiology", etc.',
        required=True,
    )
    description = fields.Text()
    active = fields.Boolean(
        default=True,
    )
