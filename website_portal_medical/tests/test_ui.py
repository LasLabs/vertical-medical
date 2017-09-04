# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.tests.common import HttpCase


class TestUi(HttpCase):

    def test_my_medical(self):
        """ It should load all the pages correctly """
        self.phantom_js(
            url_path='/my/medical',
            code='odoo.__DEBUG__.services["web_tour.tour"]'
                 '.run("website_portal_medical.my_medical_tour")',
            ready='odoo.__DEBUG__.services["web_tour.tour"]'
                  '.tours["website_portal_medical.my_medical_tour"].ready',
            login='portal',
        )
