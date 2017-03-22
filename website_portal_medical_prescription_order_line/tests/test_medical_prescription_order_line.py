# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestMedicalPrescriptionOrderLine(TransactionCase):

    def setUp(self):
        super(TestMedicalPrescriptionOrderLine, self).setUp()
        self.rx_line_1 = self.env.ref(
            'medical_prescription.'
            'medical_prescription_order_order_line_1'
        )

    def test_default_is_expired(self):
        """Rx line should not be expired if there is no stop date"""
        self.assertEquals(
            self.rx_line_1.is_expired, False
        )

    def test_expired_rx_line(self):
        """Rx line should be expired if stop date has passed"""
        self.rx_line_1.write(
            {'date_stop_treatment': "2000-01-01 12:00:00"}
        )
        self.assertTrue(self.rx_line_1.is_expired)

    def test_not_expired_rx_line(self):
        """Rx line should not be expired if stop date has not passed"""
        self.rx_line_1.write(
            {'date_stop_treatment': "3000-01-01 12:00:00"}
        )
        self.assertEquals(
            self.rx_line_1.is_expired, False
        )
