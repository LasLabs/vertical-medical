# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import TransactionCase

import mock


class TestMedicalInsuranceCompany(TransactionCase):

    def setUp(self):
        super(TestMedicalInsuranceCompany, self).setUp()
        self.company = self.env.ref(
            'medical_insurance.medical_insurance_company_1'
        )

    def test_compute_verified_by_id(self):
        """ Test verified_by_id properly set to user """
        self.company.is_verified = True
        self.assertTrue(
            self.company.verified_by_id,
        )

    @mock.patch('odoo.addons.sale_medical_prescription.'
                'models.medical_pharmacy.fields.Datetime')
    def test_compute_verified_date(self, mock_datetime):
        """ Test verified_date set with datetime """
        exp = '2016-12-13 05:15:23'
        mock_datetime.now.return_value = exp
        self.company.is_verified = True
        res = self.company.verified_date
        self.assertEquals(
            res, exp,
        )
