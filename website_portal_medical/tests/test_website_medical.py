# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import TransactionCase

from ..controllers.main import WebsiteMedical


class TestWebsiteMedical(TransactionCase):

    def setUp(self):
        super(TestWebsiteMedical, self).setUp()
        self.WebsiteMedical = WebsiteMedical()
        self.patient_1 = self.env.ref(
            'website_portal_medical.medical_patient_1'
        )

    def test_date(self):
        """ It should format date to MM/DD/YYYY """
        res = self.WebsiteMedical._format_date(
            date='2017-12-10',
        )
        exp = '12/10/2017'
        self.assertEqual(
            res,
            exp,
        )
