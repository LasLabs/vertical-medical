# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from mock import call, patch
from odoo.tests.common import TransactionCase

MODEL_PATH = (
    'odoo.addons.sale_medical_prescription_auto.models'
    '.medical_prescription_order_line.MedicalPrescriptionOrderLine'
)
AUTO_PATH = MODEL_PATH + '._sale_crm_auto'
MATCH_PATH = MODEL_PATH + '._sale_line_matches'
CONFIRM_PATH = 'odoo.addons.sale.models.sale.SaleOrder.action_confirm'


class TestMedicalPrescriptionOrderLine(TransactionCase):
    def setUp(self):
        super(TestMedicalPrescriptionOrderLine, self).setUp()

        self.test_model = self.env['medical.prescription.order.line']
        self.test_rx_line = self.env.ref(
            'sale_medical_prescription_auto'
            '.medical_prescription_order_line_1_demo'
        )
        self.test_rx_line_2 = self.env.ref(
            'sale_medical_prescription_auto'
            '.medical_prescription_order_line_2_demo'
        )
        self.test_rx_line_set = self.test_rx_line + self.test_rx_line_2

        self.hold_line_state = self.env.ref(
            'medical_prescription_state.prescription_order_line_state_hold'
        )
        self.exception_line_state = self.env.ref(
            'medical_prescription_state'
            '.prescription_order_line_state_exception'
        )

        self.test_sale_order = self.env.ref(
            'sale_medical_prescription_auto.sale_order_1_demo'
        )
        self.test_sale_line = self.env.ref(
            'sale_medical_prescription_auto.sale_order_line_1_demo'
        )
        self.test_sale_line_2 = self.env.ref(
            'sale_medical_prescription_auto.sale_order_line_2_demo'
        )

    @patch(AUTO_PATH, autospec=True)
    def test_write_move_to_verified(self, auto_mock):
        """It should call helper on Rx lines that move into verified state"""
        self.test_rx_line.stage_id = self.hold_line_state
        self.test_rx_line_2.stage_id = self.exception_line_state

        result_mock_calls = auto_mock.call_args_list
        self.assertEqual(len(result_mock_calls), 2)
        self.assertEqual(result_mock_calls[0], call(self.test_rx_line))
        self.assertEqual(result_mock_calls[1], call(self.test_model))

    @patch(AUTO_PATH, autospec=True)
    def test_write_already_verified(self, auto_mock):
        """It should not call helper on Rx lines already in verified state"""
        self.test_rx_line_set.write({'stage_id': self.hold_line_state.id})
        auto_mock.reset_mock()
        self.test_rx_line.stage_id = self.hold_line_state
        self.test_rx_line_2.stage_id = self.exception_line_state

        self.assertEqual(auto_mock.call_count, 2)
        self.assertEqual(auto_mock.call_args_list[0], call(self.test_model))
        self.assertEqual(auto_mock.call_args_list[1], call(self.test_model))

    @patch(MATCH_PATH)
    def test_sale_crm_auto_confirmed_sale_lines(self, match_mock):
        """It should mark sale order lines confirmed if helper returns True"""
        match_mock.return_value = True
        self.test_rx_line._sale_crm_auto()

        self.assertEqual(self.test_sale_line.sale_crm_auto_state, 'confirmed')

    @patch(MATCH_PATH)
    def test_sale_crm_auto_exception_sale_lines(self, match_mock):
        """It should mark sale lines as exceptions if helper returns False"""
        match_mock.return_value = False
        self.test_rx_line._sale_crm_auto()

        self.assertEqual(self.test_sale_line.sale_crm_auto_state, 'exception')

    @patch(CONFIRM_PATH, autospec=True)
    @patch(MATCH_PATH)
    def test_sale_crm_auto_confirm_order(self, match_mock, confirm_mock):
        """It should call action_confirm on order if all lines confirmed"""
        match_mock.return_value = True
        self.test_sale_line_2.sale_crm_auto_state = 'confirmed'
        self.test_rx_line._sale_crm_auto()

        confirm_mock.assert_called_once_with(self.test_sale_order)

    @patch(CONFIRM_PATH)
    @patch(MATCH_PATH)
    def test_sale_crm_auto_no_confirm_order(self, match_mock, confirm_mock):
        """It should not call action_confirm if all lines not confirmed"""
        match_mock.return_value = False
        self.test_rx_line._sale_crm_auto()

        confirm_mock.assert_not_called()

    @patch(CONFIRM_PATH)
    @patch(MATCH_PATH)
    def test_sale_crm_auto_confirm_order_lock(self, match_mock, confirm_mock):
        """It should not call action_confirm if order in certain states"""
        match_mock.return_value = True
        self.test_sale_order.state = 'sale'
        self.test_rx_line._sale_crm_auto()
        self.test_sale_order.state = 'done'
        self.test_rx_line.sale_crm_auto_ran = False
        self.test_rx_line._sale_crm_auto()
        self.test_sale_order.state = 'cancel'
        self.test_rx_line.sale_crm_auto_ran = False
        self.test_rx_line._sale_crm_auto()

        confirm_mock.assert_not_called()

    def test_sale_crm_auto_mark_processed(self):
        """It should mark processed Rx lines"""
        self.test_rx_line._sale_crm_auto()

        self.assertTrue(self.test_rx_line.sale_crm_auto_ran)

    def test_sale_crm_auto_lead_gen_existing_update(self):
        """It should update matching lead when Rx lines without sale lines"""
        self.env['crm.lead'].search([]).unlink()
        test_line_partner = self.test_rx_line.patient_id.commercial_partner_id
        test_lead = self.env['crm.lead'].create({
            'name': 'Test Lead',
            'partner_id': test_line_partner.id,
            'prescription_order_line_ids': [(6, 0, [self.test_rx_line_2.id])],
            'type': 'opportunity',
        })
        self.test_sale_line.unlink()
        self.test_rx_line._sale_crm_auto()

        result_lead_rxs = test_lead.prescription_order_line_ids
        self.assertEqual(result_lead_rxs, self.test_rx_line_set)

    def test_sale_crm_auto_lead_gen_existing_message(self):
        """It should add message when updating matching lead"""
        self.env['crm.lead'].search([]).unlink()
        test_line_partner = self.test_rx_line.patient_id.commercial_partner_id
        test_lead = self.env['crm.lead'].create({
            'name': 'Test Lead',
            'partner_id': test_line_partner.id,
            'prescription_order_line_ids': [(6, 0, [self.test_rx_line_2.id])],
            'type': 'opportunity',
        })
        test_lead.message_ids.unlink()
        self.test_sale_line.unlink()
        self.test_rx_line._sale_crm_auto()

        self.assertEqual(len(test_lead.message_ids), 1)
        self.assertEqual(test_lead.message_ids.message_type, 'notification')

    def test_sale_crm_auto_lead_gen_no_existing(self):
        """It should generate new leads when no matching leads available"""
        self.env['crm.lead'].search([]).unlink()
        self.test_sale_line.unlink()
        self.test_rx_line._sale_crm_auto()
        result_lead = self.env['crm.lead'].search([])

        test_line_partner = self.test_rx_line.patient_id.commercial_partner_id
        self.assertEqual(result_lead.partner_id, test_line_partner)
        result_lead_rxs = result_lead.prescription_order_line_ids
        self.assertEqual(result_lead_rxs, self.test_rx_line)
        self.assertEqual(result_lead.type, 'opportunity')

    def test_sale_crm_auto_lead_gen_grouping(self):
        """It should group Rx lines into leads based on commercial partner"""
        self.env['crm.lead'].search([]).unlink()
        (self.test_sale_line + self.test_sale_line_2).unlink()
        test_line_partner = self.test_rx_line.patient_id.commercial_partner_id
        self.test_rx_line_2.patient_id.partner_id = test_line_partner
        self.test_rx_line_set._sale_crm_auto()
        result_lead = self.env['crm.lead'].search([])

        self.assertEqual(result_lead.partner_id, test_line_partner)
        result_lead_rxs = result_lead.prescription_order_line_ids
        self.assertEqual(result_lead_rxs, self.test_rx_line_set)

    @patch(MATCH_PATH)
    def test_sale_crm_auto_skip_sale_lines(self, match_mock):
        """It should not make sale line changes if Rx line processed before"""
        match_mock.return_value = True
        self.test_rx_line.sale_crm_auto_ran = True
        self.test_rx_line._sale_crm_auto()

        result_sale_line_state = self.test_sale_line.sale_crm_auto_state
        self.assertEqual(result_sale_line_state, 'unprocessed')

    @patch(CONFIRM_PATH)
    def test_sale_crm_auto_skip_sale_orders(self, confirm_mock):
        """It should not make sale order changes if Rx line processed before"""
        self.test_sale_line.sale_crm_auto_state = 'confirmed'
        self.test_rx_line.sale_crm_auto_ran = True
        self.test_rx_line._sale_crm_auto()

        confirm_mock.assert_not_called()

    def test_sale_crm_auto_skip_lead_gen(self):
        """It should not generate any leads if Rx line processed before"""
        self.env['crm.lead'].search([]).unlink()
        self.test_sale_line.unlink()
        self.test_rx_line.sale_crm_auto_ran = True
        self.test_rx_line._sale_crm_auto()
        result_lead = self.env['crm.lead'].search([])

        self.assertFalse(result_lead)

    def test_sale_line_matches_multiple_rx_lines(self):
        """It should raise exception if called with multiple Rx lines"""
        with self.assertRaisesRegexp(ValueError, 'Expected singleton'):
            self.test_rx_line_set._sale_line_matches(self.test_sale_line)

    def test_sale_line_matches_different_partners(self):
        """It should return False if lines have different commercial partner"""
        self.test_sale_order.partner_id = self.env.ref('base.main_partner')
        result = self.test_rx_line._sale_line_matches(self.test_sale_line)

        self.assertFalse(result)

    def test_sale_line_matches_different_products(self):
        """It should return False if lines have different products"""
        test_product = self.env['product.product'].create({
            'name': 'Test Product',
        })
        test_line_force = self.test_sale_line.with_context(__rx_force__=True)
        test_line_force.product_id = test_product
        result = self.test_rx_line._sale_line_matches(self.test_sale_line)

        self.assertFalse(result)

    def test_sale_line_matches_qty_too_large(self):
        """It should return False if sale line qty cannot be dispensed"""
        test_line_force = self.test_sale_line.with_context(__rx_force__=True)
        test_line_force.product_uom_qty = 1000
        result = self.test_rx_line._sale_line_matches(self.test_sale_line)

        self.assertFalse(result)

    def test_sale_line_matches_all_conditions_satisfied(self):
        """It should return True if all conditions are satisfied"""
        result = self.test_rx_line._sale_line_matches(self.test_sale_line)

        self.assertTrue(result)
