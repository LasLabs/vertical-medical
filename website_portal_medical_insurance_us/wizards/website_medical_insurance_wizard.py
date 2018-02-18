# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


import logging
_logger = logging.getLogger(__name__)


class WebsiteMedicalInsuranceWizard(models.TransientModel):
    _name = 'website.medical.insurance.wizard'
    _description = 'Website Medical Insurance Wizard'

    patient_id = fields.Many2one(
        string='Patient Record',
        comodel_name='medical.patient',
        compute='_compute_patient_id',
    )
    patient_name = fields.Char(
        string='Name of Insured',
        required=True,
    )
    insurance_company_id = fields.Many2one(
        string='Insurance Company Record',
        comodel_name='medical.insurance.company',
        compute='_compute_insurance_company_id',
    )
    insurance_company_name = fields.Char(
        string='Insurance Company',
        comodel_name='medical.insurance.company',
        required=True,
    )
    number = fields.Char(
        string='Identification Number',
        required=True,
    )
    group_number = fields.Char(
        required=True,
    )
    rx_bin = fields.Char(
        required=True,
    )
    rx_pcn = fields.Char(
        string='Rx PCN',
        required=True,
    )
    rx_group = fields.Char(
        required=True,
    )
    plan_number = fields.Char(
        required=True,
    )
    plan_id = fields.Many2one(
        string='Insurance Plan',
        comodel_name='medical.insurance.plan',
    )

    @api.multi
    @api.depends('patient_name')
    def _compute_patient_id(self):
        Patients = self.env['medical.patient']
        for record in self:
            patient = Patients.search([
                ('name', '=', record.patient_name),
            ])
            if not patient:
                patient = Patients.create({
                    'name': record.patient_name,
                    'parent_id': self.env.user.partner_id.id,
                })
            record.patient_id = patient[:1]

    @api.multi
    @api.depends('insurance_company_name')
    def _compute_insurance_company_id(self):
        InsuranceCompanies = self.env['medical.insurance.company']
        for record in self:
            company = InsuranceCompanies.search([
                ('name', '=', record.insurance_company_name),
            ])
            if not company:
                company = InsuranceCompanies.create({
                    'name': record.insurance_company_name,
                    'create_uid': self.env.user.id,
                })
            record.insurance_company_id = company[:1]

    @api.model
    def create(self, vals):
        wizard = super(WebsiteMedicalInsuranceWizard, self).create(vals)
        wizard.upsert_plan()
        return wizard

    @api.multi
    def get_or_create_template(self):

        Templates = self.env['medical.insurance.template']
        template = Templates.search([
            ('insurance_company_id', '=', self.sudo().insurance_company_id.id),
            ('group_number', '=', self.group_number),
            ('rx_bin', '=', self.rx_bin),
            ('rx_pcn', '=', self.rx_pcn),
            ('rx_group', '=', self.rx_group),
            ('plan_number', '=', self.plan_number),
        ])

        if not template:
            website = self.env['website'].get_current_website()
            template = Templates.sudo().create({
                'insurance_company_id': self.sudo().insurance_company_id.id,
                'group_number': self.group_number,
                'rx_bin': self.rx_bin,
                'rx_group': self.rx_group,
                'rx_pcn': self.rx_pcn,
                'product_id': website.default_insurance_product_id.id,
                'plan_number': self.plan_number,
                'name': '[%s] %s' % (
                    self.insurance_company_name, self.plan_number,
                ),
                'create_uid': self.env.uid,
                'write_uid': self.env.uid,
            })

        return template[:1]

    @api.multi
    def upsert_plan(self):

        template = self.get_or_create_template()
        vals = {
            'patient_id': self.sudo().patient_id.id,
            'insurance_template_id': template.id,
            'number': self.number,
        }

        if self.plan_id:
            self.plan_id.write(vals)
            return self.plan_id

        Plans = self.env['medical.insurance.plan']
        plan = Plans.search([
            ('patient_id', '=', self.sudo().patient_id.id),
            ('insurance_template_id', '=', template.id),
            ('number', '=', self.number),
        ])

        if not plan:
            plan = Plans.sudo().create(vals)

        return plan[:1]
