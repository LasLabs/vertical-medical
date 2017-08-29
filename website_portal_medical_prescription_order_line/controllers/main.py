# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import http
from odoo.http import request

from odoo.addons.website_portal_medical.controllers.main import (
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
        """ Add prescription counter to medical account page """
        response = super(WebsiteMedical, self).my_medical()
        partner_id = request.env.user.partner_id
        rx_obj = request.env['medical.prescription.order.line']
        rx_line_count = rx_obj.search_count([
            ('patient_id.parent_id', 'child_of', [partner_id.id]),
        ])
        response.qcontext.update({
            'rx_line_count': rx_line_count,
        })
        return response

    @http.route(
        ['/medical/prescriptions'],
        type='http',
        auth="user",
        website=True,
    )
    def medical_prescriptions(self, **kw):
        partner_id = request.env.user.partner_id

        rx_obj = request.env['medical.prescription.order.line']
        patient_model = request.env['medical.patient']

        rx_line_ids = rx_obj.search([
            ('patient_id.parent_id', 'child_of', [partner_id.id]),
        ])

        patient_ids = request.httprequest.args.getlist('patients')
        int_patient_ids = [int(id) for id in patient_ids]
        filtered_patients = patient_model.browse(int_patient_ids)
        if filtered_patients:
            rx_line_ids = rx_line_ids.filtered(
                lambda r: r.patient_id in filtered_patients,
            )

        pricelist = request.website.get_current_pricelist()
        pricelist_item_ids = pricelist.item_ids.ids

        rx_lines_filtered = rx_obj.sudo().search([
            ('id', 'in', rx_line_ids.ids),
            ('medicament_id.item_ids', 'in', pricelist_item_ids),
        ])

        all_patients = patient_model._search_related_patients()

        values = ({
            'prescription_order_lines': rx_line_ids.sudo(),
            'order_lines_filtered': rx_lines_filtered,
            'patients_filtered': filtered_patients,
            'patients_not_filtered': all_patients - filtered_patients,
            'user': request.env.user,
        })
        return request.render(
            'website_portal_medical_prescription_order_line.'
            'prescription_lines', values,
        )
