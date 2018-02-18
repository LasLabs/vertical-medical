# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class MedicalInsurancePlan(models.Model):

    _name = 'medical.insurance.plan'
    _inherit = ['medical.insurance.plan',
                'website.published.mixin',
                'mail.thread',
                ]

    @api.multi
    def action_invalidate(self):
        return self.write({'member_exp': fields.Date.today()})

    @api.multi
    def _compute_website_url(self):
        for record in self:
            record.website_url = "/medical/insurance/plan/%d" % (record.id)

    @api.model
    def search_related_patient_medical_plans(self, patients=None):

        if not patients:
            patients = self.env['medical.patient'].search_related_patients()

        date_now = fields.Date.today()

        insurance_plans = patients.mapped('insurance_plan_ids').sorted(
            lambda r: r.insurance_template_id.sudo().insurance_company_id.name,
        )

        active_plans = insurance_plans.filtered(
            lambda r: not r.member_exp or r.member_exp > date_now
        )

        return active_plans
