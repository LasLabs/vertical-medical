# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from openerp.tests.common import HttpCase


class TestUi(HttpCase):
    def test_patient_filter(self):
        """Should have correct UI elements and interactivity"""
        self.phantom_js(
            url_path='/my/medical',
            code='odoo.__DEBUG__.services["web_tour.tour"]'
                 '.run("website_portal_medical_prescription_order_line'
                 '.patient_filter_tour")',
            ready='odoo.__DEBUG__.services["web_tour.tour"]'
                  '.tours["website_portal_medical_prescription_order_line'
                  '.patient_filter_tour"].ready',
            login='admin',
        )
