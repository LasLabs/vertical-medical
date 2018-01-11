# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from mock import patch
from odoo.tests.common import TransactionCase

NOW_PATH = (
    'odoo.addons.sale_medical_prescription_auto.models.sale_order_line'
    '.fields.Datetime.now'
)


@patch(NOW_PATH)
class TestSaleOrderLine(TransactionCase):
    def setUp(self):
        super(TestSaleOrderLine, self).setUp()

        self.test_sale_line = self.env.ref(
            'sale_medical_prescription_auto.sale_order_line_1_demo'
        )

    def test_compute_sale_crm_auto_state_changed_on_change(self, now_mock):
        """It should set value to current time when state changes"""
        now_mock.return_value = test_time = '2018-01-05 00:00:00'
        self.test_sale_line.sale_crm_auto_state = 'confirmed'

        result_time = self.test_sale_line.sale_crm_auto_state_changed
        self.assertEqual(result_time, test_time)

    def test_compute_sale_crm_auto_state_changed_on_access(self, now_mock):
        """It should not recompute value on access"""
        now_mock.return_value = test_time = '2018-01-05 00:00:00'

        result_time = self.test_sale_line.sale_crm_auto_state_changed
        self.assertNotEqual(result_time, test_time)
