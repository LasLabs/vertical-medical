# -*- coding: utf-8 -*-
# Copyright 2018 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import api, fields, models


class MedicalPatient(models.Model):
    _inherit = 'medical.patient'

    diagnostic_report_ids = fields.One2many(
        string='Diagnostic Reports',
        comodel_name='medical.diagnostic.report',
        inverse_name='patient_id',
    )
    diagnostic_request_ids = fields.One2many(
        string='Diagnostic Requests',
        comodel_name='medical.diagnostic.request',
        inverse_name='patient_id',
    )
    diagnostic_report_count = fields.Integer(
        string='Diagnostic Report Count',
        compute='_compute_diagnostic_report_count',
    )
    diagnostic_request_count = fields.Integer(
        string='Diagnostic Request Count',
        compute='_compute_diagnostic_request_count',
    )

    @api.multi
    @api.depends('diagnostic_report_ids')
    def _compute_diagnostic_report_count(self):
        for record in self:
            record.diagnostic_report_count = len(record.diagnostic_report_ids)

    @api.multi
    @api.depends('diagnostic_request_ids')
    def _compute_diagnostic_request_count(self):
        for record in self:
            diagnostic_requests = record.diagnostic_request_ids
            record.diagnostic_request_count = len(diagnostic_requests)
