# -*- coding: utf-8 -*-
# Copyright 2018 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import TransactionCase


class TestMedicalPatient(TransactionCase):

    def setUp(self):
        super(TestMedicalPatient, self).setUp()

        self.test_patient = self.env.ref(
            'medical_diagnostic.medical_patient_1_demo'
        )
        self.test_patient_2 = self.env.ref(
            'medical_diagnostic.medical_patient_2_demo'
        )

    def test_compute_diagnostic_report_count(self):
        """It should set field to count of patient's diagnostic reports"""
        self.assertEqual(self.test_patient.diagnostic_report_count, 1)
        self.assertEqual(self.test_patient_2.diagnostic_report_count, 0)

    def test_compute_diagnostic_request_count(self):
        """It should set field to count of patient's diagnostic requests"""
        self.assertEqual(self.test_patient.diagnostic_request_count, 1)
        self.assertEqual(self.test_patient_2.diagnostic_request_count, 0)
