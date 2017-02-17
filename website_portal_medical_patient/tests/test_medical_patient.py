# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestMedicalPatient(TransactionCase):

    def setUp(self):
        super(TestMedicalPatient, self).setUp()
        self.patient_1 = self.env.ref(
            'website_portal_medical_patient.medical_patient_1'
        )

    def test_compute_website_url(self):
        """ Test website_url returns correct id """
        self.assertEquals(
            self.patient_1.website_url,
            '/medical/patients/%s' % self.patient_1.id,
        )
