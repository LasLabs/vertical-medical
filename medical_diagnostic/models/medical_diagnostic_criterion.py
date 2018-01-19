# -*- coding: utf-8 -*-
# Copyright 2012-2013 Federico Manuel Echeverri Choux
# Copyright 2016-2018 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class MedicalDiagnosticCriterion(models.Model):
    _name = 'medical.diagnostic.criterion'
    _description = 'Medical Diagnostic Criterion'

    name = fields.Char(
        required=True,
    )
    description = fields.Text()
    result_expect = fields.Char(
        string='Normal Value(s)',
        required=True,
    )
    uom_id = fields.Many2one(
        string='Unit of Measure',
        comodel_name='product.uom',
        ondelete='restrict',
    )
    category_id = fields.Many2one(
        string='Diagnostic Category',
        comodel_name='medical.diagnostic.category',
        ondelete='restrict',
        help='The diagnostic category that this criterion applies to',
        required=True,
    )
    active = fields.Boolean(
        default=True,
    )
