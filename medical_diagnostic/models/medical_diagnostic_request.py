# -*- coding: utf-8 -*-
# Copyright 2016-2018 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class MedicalDiagnosticRequest(models.Model):
    _name = 'medical.diagnostic.request'
    _description = 'Medical Diagnostic Request'
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Requests must have a unique ID!'),
    ]

    name = fields.Char(
        string='ID',
        required=True,
        default=lambda s: s.env['ir.sequence'].next_by_code(
            'medical.diagnostic.request',
        ),
        help='Unique identifier for request',
    )
    category_id = fields.Many2one(
        string='Diagnostic Category',
        comodel_name='medical.diagnostic.category',
        help='General category of diagnostic services in request',
        required=True,
        ondelete='restrict',
    )
    requester_id = fields.Many2one(
        string='Request Creator',
        comodel_name='medical.practitioner',
        help='Medical practitioner that created the request',
    )
    report_ids = fields.One2many(
        string='Diagnostic Reports',
        comodel_name='medical.diagnostic.report',
        inverse_name='request_id',
        help='Diagnostic reports generated based on this request',
    )
    date_request = fields.Datetime(
        string='Request Date',
        default=lambda s: fields.Datetime.now(),
    )
    notes = fields.Text(
        string='Additional Notes',
    )
    patient_id = fields.Many2one(
        string='Request Subject',
        comodel_name='medical.patient',
        help='Patient associated with request',
        required=True,
        ondelete='cascade',
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('done', 'Completed'),
            ('cancel', 'Cancelled'),
        ],
        default='draft',
        required=True,
    )
    procedure_ids = fields.Many2many(
        string='Procedures',
        comodel_name='medical.procedure',
        help='The diagnostic procedures that are being requested',
    )
