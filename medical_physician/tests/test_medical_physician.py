# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestMedicalPhysician(TransactionCase):

    def setUp(self):
        super(TestMedicalPhysician, self).setUp()
        vals = {
            'name': 'Test Specialty',
        }
        specialty_id = self.env['medical.specialty'].create(vals)
        vals = {
            'name': 'Test Physician',
            'specialty_id': specialty_id.id,
        }
        self.physician_id = self.env['medical.physician'].create(vals)

    def test_is_doctor(self):
        """ Test physician is doctor """
        self.assertTrue(
            self.physician_id.is_doctor,
            'Should be True.\rGot: %s\rExpected: %s' % (
                self.physician_id.is_doctor, True
            )
        )

    def test_sequence(self):
        """ Test physician code is set to sequence if None """
        self.assertTrue(
            self.physician_id.code,
            'Code should be set to sequence if None.\rGot: %s\rExpected: %s' % (
                self.physician_id.code, 'TS'
            )
        )

    def test_physician_customer(self):
        """ Test customer set to False when creating physician """
        self.assertFalse(
            self.physician_id.customer,
            'Customer should be False.\rGot: %s\rExpected: %s' % (
                self.physician_id.code, False
            )
        )
