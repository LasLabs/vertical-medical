# -*- coding: utf-8 -*-
# Copyright 2012-2013 Federico Manuel Echeverri Choux
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class MedicalDiagnosticObservation(models.Model):
    _name = 'medical.diagnostic.observation'
    _description = 'Medical Diagnostic Observation'

    criterion_id = fields.Many2one(
        string='Base Criterion',
        comodel_name='medical.diagnostic.criterion',
        required=True,
        ondelete='restrict',
        domain='[("category_id", "=", report_category_id)]',
    )
    result_expect = fields.Char(
        related='criterion_id.result_expect',
        readonly=True,
    )
    uom_id = fields.Many2one(
        related='criterion_id.uom_id',
        readonly=True,
    )
    category_id = fields.Many2one(
        related='criterion_id.category_id',
        readonly=True,
    )
    result_actual = fields.Char(
        string='Result',
        required=True,
    )
    report_id = fields.Many2one(
        string='Diagnostic Report',
        comodel_name='medical.diagnostic.report',
        required=True,
        ondelete='cascade',
    )
    report_category_id = fields.Many2one(
        related='report_id.category_id',
        readonly=True,
    )
    notes = fields.Text()
