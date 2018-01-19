# -*- coding: utf-8 -*-
# Copyright 2012-2013 Federico Manuel Echeverri Choux
# Copyright 2016-2018 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class MedicalDiagnosticReport(models.Model):
    _name = 'medical.diagnostic.report'
    _description = 'Medical Diagnostic Report'
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Reports must have a unique ID!'),
    ]

    name = fields.Char(
        string='ID',
        required=True,
        default=lambda s: s.env['ir.sequence'].next_by_code(
            'medical.diagnostic.report',
        ),
        help='Unique identifier for report',
    )
    category_id = fields.Many2one(
        help='General category of diagnostic services in report',
        related='request_id.category_id',
        readonly=True,
    )
    performer_id = fields.Many2one(
        string='Report Creator',
        comodel_name='res.partner',
        help='Person or company that performed exams and created the report',
    )
    request_id = fields.Many2one(
        string='Diagnostic Request',
        comodel_name='medical.diagnostic.request',
        help='Diagnostic request that prompted creation of report',
        required=True,
        ondelete='restrict',
    )
    date_analysis = fields.Datetime(
        string='Analysis Date',
        default=lambda s: fields.Datetime.now(),
    )
    date_report = fields.Datetime(
        string='Report Date',
        default=lambda s: fields.Datetime.now(),
    )
    result_ids = fields.One2many(
        string='Diagnostic Results',
        comodel_name='medical.diagnostic.observation',
        inverse_name='report_id',
    )
    diagnosis_ids = fields.Many2many(
        string='Diagnoses',
        comodel_name='medical.pathology',
        help='Pathologies diagnosed in this report',
    )
    notes = fields.Text(
        string='Additional Notes',
    )
    patient_id = fields.Many2one(
        related='request_id.patient_id',
        readonly=True,
        string='Report Subject',
        help='Patient associated with report',
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('done', 'Completed'),
        ],
        default='draft',
        required=True,
    )
