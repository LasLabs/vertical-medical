# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from mock import patch
from odoo.tests.common import TransactionCase

AUTO_PATH = (
    'odoo.addons.sale_medical_prescription_auto.models'
    '.medical_prescription_order_line.MedicalPrescriptionOrderLine'
    '._sale_crm_auto'
)


@patch(AUTO_PATH, autospec=True)
class TestMedicalPrescriptionOrderLine(TransactionCase):
    def setUp(self):
        super(TestMedicalPrescriptionOrderLine, self).setUp()

        self.rx_line_model = self.env['medical.prescription.order.line']
        self.test_rx_line = self.env.ref(
            'sale_medical_prescription_auto'
            '.medical_prescription_order_line_1_demo'
        )

        self.hold_line_state = self.env.ref(
            'medical_prescription_state.prescription_order_line_state_hold'
        )
        self.exception_line_state = self.env.ref(
            'medical_prescription_state'
            '.prescription_order_line_state_exception'
        )

    def test_write_stage_newly_verified(self, auto_mock):
        """It should call helper on Rx lines in newly verified state"""
        self.rx_line_model.search([
            ('stage_id', '=', self.exception_line_state.id),
        ]).unlink()
        self.test_rx_line.stage_id = self.exception_line_state
        auto_mock.reset_mock()
        self.exception_line_state.is_verified = True

        auto_mock.assert_called_once_with(self.test_rx_line)

    def test_write_stage_already_verified(self, auto_mock):
        """It should not call helper on Rx lines in already verified state"""
        self.rx_line_model.search([
            ('stage_id', '=', self.hold_line_state.id),
        ]).unlink()
        self.test_rx_line.stage_id = self.hold_line_state
        auto_mock.reset_mock()
        self.hold_line_state.name = 'Test Name'

        auto_mock.assert_called_once_with(self.rx_line_model)

    def test_write_stage_newly_unverified(self, auto_mock):
        """It should not call helper on Rx lines in newly unverified state"""
        self.rx_line_model.search([
            ('stage_id', '=', self.hold_line_state.id),
        ]).unlink()
        self.test_rx_line.stage_id = self.hold_line_state
        auto_mock.reset_mock()
        self.hold_line_state.is_verified = False

        auto_mock.assert_called_once_with(self.rx_line_model)

    def test_write_stage_already_unverified(self, auto_mock):
        """It should not call helper on Rx lines in already unverified state"""
        self.rx_line_model.search([
            ('stage_id', '=', self.exception_line_state.id),
        ]).unlink()
        self.test_rx_line.stage_id = self.exception_line_state
        auto_mock.reset_mock()
        self.exception_line_state.name = 'Test Name'

        auto_mock.assert_called_once_with(self.rx_line_model)
