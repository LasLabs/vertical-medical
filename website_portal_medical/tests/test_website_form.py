# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import TransactionCase

from ..controllers.main import WebsiteForm


class TestWebsiteForm(TransactionCase):

    def setUp(self):
        super(TestWebsiteForm, self).setUp()
        self.WebsiteForm = WebsiteForm()
        self.patient_1 = self.env.ref(
            'website_portal_medical.medical_patient_1'
        )

    def test_date(self):
        """ It should format date back to default format """
        res = self.WebsiteForm.date(
            field_label='test',
            field_input='12/10/2017',
        )
        exp = '2017-12-10'
        self.assertEqual(
            res,
            exp,
        )
