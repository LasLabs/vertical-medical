# -*- coding: utf-8 -*-
# © 2016-TODAY LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

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

        patient_ids = request.httprequest.args.getlist("patients")
        if len(patient_ids) > 0:
            int_patient_ids = []
            for id in patient_ids:
                int_patient_ids.append(int(id))
            rx_line_ids = rx_line_ids.search([
                ('patient_id', 'in', int_patient_ids),
            ])

        pricelist = request.website.get_current_pricelist()
        pricelist_item_ids = pricelist.item_ids.ids

        rx_lines_filtered = rx_line_ids.filtered(
            lambda r: any(
                i in r.medicament_id.item_ids.ids for i in pricelist_item_ids
            )
        )

        response.qcontext.update({
            'prescription_order_lines': rx_line_ids.sudo(),
            'order_lines_filtered': rx_lines_filtered,
        })
        return response

    @http.route(
        '/medical/prescription/<int:rx_id>',
        type='http',
        auth='user',
        website=True,
        methods=['GET'],
    )
    def prescription_show(self, rx_id, **kwargs):
        # values = {
        #     'error': {},
        #     'error_message': [],
        #     'success_page': kwargs.get('success_page', '/my/medical')
        # }
        raise NotImplementedError()

    @http.route(
        ['/medical/prescription/<int:rx_id>/line/<int:rx_line_id>'],
        type='http',
        auth='user',
        website=True,
        methods=['GET'],
    )
    def prescription_line_show(self, rx_id, rx_line_id, **kwargs):
        # values = {
        #     'error': {},
        #     'error_message': [],
        #     'success_page': kwargs.get('success_page', '/my/medical')
        # }
        raise NotImplementedError()
