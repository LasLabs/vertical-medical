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
        website=True
    )
    def my_medical(self, **kw):
        """ Add prescriptions to medical account page """
        response = super(WebsiteMedical, self).my_medical()
        partner_id = request.env.user.partner_id

        rx_obj = request.env['medical.prescription.order.line']
        rx_line_ids = rx_obj.search([
            ('patient_id.parent_id', 'child_of', [partner_id.id]),
        ])

        patient_ids = request.httprequest.args.getlist('patients')
        int_patient_ids = [int(id) for id in patient_ids]
        patient_model = request.env['medical.patient']
        filtered_patients = patient_model.browse(int_patient_ids)
        if filtered_patients:
            rx_line_ids = rx_line_ids.filtered(
                lambda r: r.patient_id in filtered_patients,
            )

        pricelist = request.website.get_current_pricelist()
        pricelist_item_ids = pricelist.item_ids.ids
        rx_lines_filtered = rx_line_ids.filtered(
            lambda r: any(
                i in r.medicament_id.item_ids.ids for i in pricelist_item_ids
            )
        )

        all_patients = response.qcontext.get('patients', patient_model)
        response.qcontext.update({
            'prescription_order_lines': rx_line_ids.sudo(),
            'order_lines_filtered': rx_lines_filtered,
            'patients_filtered': filtered_patients,
            'patients_not_filtered': all_patients - filtered_patients,
        })
        return response
