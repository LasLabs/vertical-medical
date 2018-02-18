# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo.tests import HttpCase


class TestUi(HttpCase):

    def test_subtotals(self):
        code = (
            'odoo.__DEBUG__.services["web_tour.tour"].'
            'run("website_portal_medical_insurance_us.tour")'
        )
        ready = (
            'odoo.__DEBUG__.services["web_tour.tour"].tours['
            '"website_portal_medical_insurance_us.tour"].ready'
        )
        self.phantom_js(
            url_path='/my/medical',
            code=code,
            ready=ready,
            login='portal',
        )
