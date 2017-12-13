# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from mock import patch
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

MODELS_PATH = 'odoo.addons.sale_medical_prescription.models'
DATE_PATH = MODELS_PATH + '.medical_prescription_order.fields.Datetime'


class TestMedicalPrescriptionOrder(TransactionCase):
    def setUp(self):
        super(TestMedicalPrescriptionOrder, self).setUp()

        module = 'medical_prescription_state_verify'
        self.test_order = self.env.ref(
            module + '.medical_prescription_order_1_demo'
        )
        self.test_line = self.env.ref(
            module + '.medical_prescription_order_line_1_demo'
        )

        self.state_module = 'medical_prescription_state'
        self.verified_rx_state = self.env.ref(
            self.state_module + '.prescription_order_state_verified'
        )
        self.unverified_rx_state = self.env.ref(
            self.state_module + '.prescription_order_state_unverified'
        )
        self.exception_rx_state = self.env.ref(
            self.state_module + '.prescription_order_state_exception'
        )
        self.cancelled_rx_state = self.env.ref(
            self.state_module + '.prescription_order_state_cancelled'
        )
        self.exception_line_state = self.env.ref(
            self.state_module + '.prescription_order_line_state_exception'
        )

    @patch(DATE_PATH)
    def test_compute_verified_move_to_verified_state(self, date_mock):
        """It should set fields correctly when Rx moved to verified state"""
        date_mock.now.return_value = test_date = '2017-11-29 12:00:00'
        self.test_order.stage_id = self.verified_rx_state

        self.assertTrue(self.test_order.is_verified)
        self.assertEqual(self.test_order.verify_user_id, self.env.user)
        self.assertEqual(self.test_order.verify_date, test_date)

    def test_compute_verified_move_to_unverified_state(self):
        """It should set fields to False when Rx moved to unverified state"""
        self.test_order.stage_id = self.verified_rx_state
        self.test_order.stage_id = self.exception_rx_state

        self.assertFalse(self.test_order.is_verified)
        self.assertFalse(self.test_order.verify_user_id)
        self.assertFalse(self.test_order.verify_date)

    def test_compute_verified_state_becomes_unverified(self):
        """It should set fields to False when Rx state becomes unverified"""
        self.test_order.stage_id = self.verified_rx_state
        self.verified_rx_state.is_verified = False

        self.assertFalse(self.test_order.is_verified)
        self.assertFalse(self.test_order.verify_user_id)
        self.assertFalse(self.test_order.verify_date)

    @patch(DATE_PATH)
    def test_compute_verified_state_becomes_verified(self, date_mock):
        """It should set fields correctly when Rx state becomes verified"""
        date_mock.now.return_value = test_date = '2017-11-29 12:00:00'
        self.unverified_rx_state.is_verified = True

        self.assertTrue(self.test_order.is_verified)
        self.assertEqual(self.test_order.verify_user_id, self.env.user)
        self.assertEqual(self.test_order.verify_date, test_date)

    def test_inverse_is_verified_false_and_unverified(self):
        """It should do nothing if set to False and state unverified"""
        self.test_order.is_verified = False

        self.assertEqual(self.test_order.stage_id, self.unverified_rx_state)

    def test_inverse_is_verified_false_and_verified(self):
        """It should set state to exception if set to False when verified"""
        self.test_order.stage_id = self.verified_rx_state
        self.test_order.is_verified = False

        self.assertEqual(self.test_order.stage_id, self.exception_rx_state)

    def test_inverse_is_verified_true_and_unverified(self):
        """It should update state if set to True and state unverified"""
        self.test_order.is_verified = True

        self.assertEqual(self.test_order.stage_id, self.verified_rx_state)

    def test_inverse_is_verified_true_and_verified(self):
        """It should do nothing if set to True and state verified"""
        self.test_order.stage_id = self.verified_rx_state
        self.test_order.is_verified = True

        self.assertEqual(self.test_order.stage_id, self.verified_rx_state)

    def test_write_restrict_content_changes_verified_rx(self):
        self.test_order.stage_id = self.verified_rx_state

        with self.assertRaisesRegexp(ValidationError, 'edit'):
            self.test_order.name = 'Test Name'

    def test_write_allow_content_changes_verified_rx_is_verified(self):
        """It should allow changes to is_verified field when state verified"""
        self.test_order.stage_id = self.verified_rx_state

        try:
            self.test_order.is_verified = False
        except ValidationError:
            self.fail('A ValidationError was raised and should not have been.')

    def test_write_allow_content_changes_verified_rx_verify_method(self):
        """It should allow changes to verify_method when state verified"""
        self.test_order.stage_id = self.verified_rx_state

        try:
            self.test_order.verify_method = 'doctor_phone'
        except ValidationError:
            self.fail('A ValidationError was raised and should not have been.')

    def test_write_restricted_state_changes_verified_rx(self):
        self.test_order.stage_id = self.verified_rx_state

        with self.assertRaisesRegexp(ValidationError, 'move'):
            self.test_order.stage_id = self.unverified_rx_state

    def test_write_allowed_state_changes_verified_rx(self):
        self.test_order.stage_id = self.verified_rx_state

        try:
            self.test_order.stage_id = self.cancelled_rx_state
        except ValidationError:
            self.fail('A ValidationError was raised and should not have been.')

    def test_write_no_limits_unverified_rx(self):
        self.test_order.stage_id = self.unverified_rx_state

        try:
            self.test_order.name = 'Test Name'
            self.test_order.stage_id = self.verified_rx_state
        except ValidationError:
            self.fail('A ValidationError was raised and should not have been.')

    def test_write_line_to_hold_when_change_to_verified(self):
        self.test_order.stage_id = self.verified_rx_state

        hold_line_state = self.env.ref(
            self.state_module + '.prescription_order_line_state_hold'
        )
        self.assertEqual(self.test_line.stage_id, hold_line_state)

    def test_write_line_to_exception_when_change_to_cancelled(self):
        self.test_order.stage_id = self.cancelled_rx_state

        self.assertEqual(self.test_line.stage_id, self.exception_line_state)

    def test_write_line_to_exception_when_change_to_exception(self):
        self.test_order.stage_id = self.exception_rx_state

        self.assertEqual(self.test_line.stage_id, self.exception_line_state)
