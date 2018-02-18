# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import http
from odoo.http import request

from odoo.addons.website_portal_medical_patient.controllers.main import (
    WebsiteMedical
)


class WebsiteMedical(WebsiteMedical):

    @http.route(
        ['/my/medical', '/medical'],
        type='http',
        auth="user",
        website=True,
    )
    def my_medical(self, **kw):
        """ Add insurances to medical account page """
        response = super(WebsiteMedical, self).my_medical()
        Plan = request.env['medical.insurance.plan']
        active_plans = Plan.search_related_patient_medical_plans(
            patients=response.qcontext['patients']
        )
        response.qcontext.update({
            'insurance_plans': active_plans.sudo(),
        })
        return response

    @http.route(
        ['/medical/insurance/plans'],
        type='http',
        auth='user',
        website=True,
        methods=['GET'],
    )
    def medical_insurance(self):
        active_plans = request.env['medical.insurance.plan'].\
            search_related_patient_medical_plans()
        values = {
            'user': request.env.user,
            'insurance_plans': active_plans,
        }
        return request.render(
            'website_portal_medical_insurance_us.insurances',
            values,
        )

    @http.route(
        ['/medical/insurance/plan/<int:plan_id>'],
        type='http',
        auth='user',
        website=True,
        methods=['GET'],
    )
    def insurance_plan_show(self, plan_id, redirect=None, **kwargs):
        values = {
            'error': {},
            'error_message': [],
            'success_page': kwargs.get(
                'success_page', '/medical/insurance/plans'
            )
        }

        plan = request.env['medical.insurance.plan'].browse(plan_id)
        if not plan:
            return request.render('website.404')

        values.update({
            'insurance_plan': plan and plan.sudo(),
        })
        return request.render(
            'website_portal_medical_insurance_us.insurance_plan', values,
        )

    @http.route(
        ['/medical/insurance/plan'],
        type='http',
        auth='user',
        website=True,
        methods=['GET'],
    )
    def insurance_plan_create_form(self, redirect=None, **kwargs):
        values = {
            'error': {},
            'error_message': [],
            'success_page': kwargs.get(
                'success_page', '/medical/insurance/plans'
            )
        }
        plan = request.env['medical.insurance.plan'].browse()
        values.update({
            'insurance_plan': plan and plan.sudo(),
        })
        return request.render(
            'website_portal_medical_insurance_us.insurance_plan', values,
        )
