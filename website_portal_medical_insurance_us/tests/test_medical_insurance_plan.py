# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import TransactionCase


class TestMedicalInsurancePlan(TransactionCase):

    def setUp(self):
        super(TestMedicalInsurancePlan, self).setUp()
        self.plan = self.env.ref(
            'medical_insurance.medical_insurance_plan_1'
        )

    def test_compute_website_url(self):
        """ Test website_url returns correct id """
        self.assertEquals(
            self.plan.website_url,
            '/medical/insurance/plan/%d' % self.plan.id,
        )
