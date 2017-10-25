# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import mock
from odoo.tests.common import TransactionCase

MODEL_PATH = 'odoo.addons.sale_medical_prescription.models'


class TestMedicalPractitioner(TransactionCase):
    def setUp(self):
        super(TestMedicalPractitioner, self).setUp()

        self.test_practitioner = self.env.ref(
            'sale_medical_prescription.medical_practitioner_5_demo'
        )

    def test_compute_verified_by_id_and_date_correct_user(self):
        """It should set verified_by_id field to correct user"""
        self.test_practitioner.is_verified = True

        self.assertEqual(self.test_practitioner.verified_by_id, self.env.user)

    @mock.patch(MODEL_PATH + '.medical_practitioner.fields.Datetime')
    def test_compute_verified_by_id_and_date_correct_date(self, datetime_mock):
        """It should set verified_date field to the correct date and time"""
        expected_date = '2016-12-13 05:15:23'
        datetime_mock.now.return_value = expected_date
        self.test_practitioner.is_verified = True

        self.assertEquals(self.test_practitioner.verified_date, expected_date)
