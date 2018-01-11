# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import TransactionCase


class TestSaleOrder(TransactionCase):
    def setUp(self):
        super(TestSaleOrder, self).setUp()

        self.test_model = self.env['sale.order']
        self.test_sale_order = self.env.ref(
            'sale_medical_prescription_auto.sale_order_1_demo'
        )

        self.test_sale_line = self.env.ref(
            'sale_medical_prescription_auto.sale_order_line_1_demo'
        )
        self.test_sale_line_2 = self.env.ref(
            'sale_medical_prescription_auto.sale_order_line_2_demo'
        )
        self.test_sale_line_set = self.test_sale_line + self.test_sale_line_2

    def test_sale_order_split_no_exceptions(self):
        """It should not split orders with no lines in exception state"""
        self.test_sale_line.sale_crm_auto_state = 'confirmed'
        self.test_model._sale_order_split()

        resulting_lines = self.test_sale_order.order_line
        self.assertEqual(resulting_lines, self.test_sale_line_set)

    def test_sale_order_split_no_confirmed(self):
        """It should not split orders with no confirmed lines"""
        self.test_sale_line.sale_crm_auto_state = 'exception'
        self.test_model._sale_order_split()

        resulting_lines = self.test_sale_order.order_line
        self.assertEqual(resulting_lines, self.test_sale_line_set)

    def test_sale_order_split_cutoff_not_met_exceptions(self):
        """It should not split orders where exceptions after time cutoff"""
        self.test_sale_line.sale_crm_auto_state = 'exception'
        self.test_sale_line_2.sale_crm_auto_state = 'confirmed'
        self.test_sale_line_2.sale_crm_auto_state_changed = '2018-01-01'
        self.test_model._sale_order_split()

        resulting_lines = self.test_sale_order.order_line
        self.assertEqual(resulting_lines, self.test_sale_line_set)

    def test_sale_order_split_cutoff_not_met_confirmations(self):
        """It should not split orders with confirmed lines after time cutoff"""
        self.test_sale_line.sale_crm_auto_state = 'exception'
        self.test_sale_line.sale_crm_auto_state_changed = '2018-01-01'
        self.test_sale_line_2.sale_crm_auto_state = 'confirmed'
        self.test_model._sale_order_split()

        resulting_lines = self.test_sale_order.order_line
        self.assertEqual(resulting_lines, self.test_sale_line_set)

    def test_sale_order_split_trigger_split(self):
        """It should split orders if line states correct before time cutoff"""
        self.test_sale_line.sale_crm_auto_state = 'exception'
        self.test_sale_line.sale_crm_auto_state_changed = '2018-01-01'
        self.test_sale_line_2.sale_crm_auto_state = 'confirmed'
        self.test_sale_line_2.sale_crm_auto_state_changed = '2018-01-01'
        self.test_model._sale_order_split()

        resulting_lines = self.test_sale_order.order_line
        self.assertEqual(resulting_lines, self.test_sale_line_2)

    def test_sale_order_split_new_order_group_exceptions(self):
        """It should group exception lines into one new order when splitting"""
        self.test_sale_line.sale_crm_auto_state = 'exception'
        self.test_sale_line_2.sale_crm_auto_state = 'confirmed'
        test_sale_line_3 = self.test_sale_line.copy({
            'order_id': self.test_sale_order.id,
        })
        self.test_sale_order.company_id.hrs_before_sale_order_split = 0
        self.test_model._sale_order_split()

        self.assertEqual(len(self.test_sale_line.order_id.order_line), 2)
        self.assertEqual(
            self.test_sale_line.order_id,
            test_sale_line_3.order_id,
        )

    def test_sale_order_split_new_order_reference_to_original(self):
        """It should give new order reference to name of original"""
        self.test_sale_line.sale_crm_auto_state = 'exception'
        self.test_sale_line_2.sale_crm_auto_state = 'confirmed'
        self.test_sale_order.company_id.hrs_before_sale_order_split = 0
        self.test_model._sale_order_split()

        new_order = self.test_sale_line.order_id
        self.assertEqual(new_order.origin, self.test_sale_order.name)

    def test_sale_order_split_new_order_copy(self):
        """It should largely make new order a copy of order being split"""
        self.test_sale_line.sale_crm_auto_state = 'exception'
        self.test_sale_line_2.sale_crm_auto_state = 'confirmed'
        self.test_sale_order.company_id.hrs_before_sale_order_split = 0
        self.test_model._sale_order_split()

        new_order_vals = self.test_sale_line.order_id.copy_data()[0]
        expected_vals = self.test_sale_order.copy_data()[0]
        del new_order_vals['origin'], new_order_vals['order_line']
        del expected_vals['origin'], expected_vals['order_line']
        self.assertEqual(new_order_vals, expected_vals)
