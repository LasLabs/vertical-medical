# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.tests.common import TransactionCase
from ..hooks import pre_init_hook, post_init_hook


class TestHooks(TransactionCase):
    def test_pre_init_hook_dummy_rx_stage_create(self):
        """It should create single dummy Rx stage"""
        old_stages = self.env['base.kanban.stage'].search([])
        pre_init_hook(self.cr)
        result_stage = self.env['base.kanban.stage'].search([
            ('res_model_id.model', '=', 'medical.prescription.order')
        ]) - old_stages

        self.assertEqual(len(result_stage), 1)

    def test_pre_init_hook_dummy_rx_line_stage_create(self):
        """It should create single dummy Rx line stage"""
        old_stages = self.env['base.kanban.stage'].search([])
        pre_init_hook(self.cr)
        result_stage = self.env['base.kanban.stage'].search([
            ('res_model_id.model', '=', 'medical.prescription.order.line')
        ]) - old_stages

        self.assertEqual(len(result_stage), 1)

    def test_post_init_hook_unverified_state_rx(self):
        """It should put all Rx records in unverified state"""
        pre_init_hook(self.cr)
        post_init_hook(self.cr, self.registry)

        rx_orders = self.env['medical.prescription.order'].search([])
        unverified_rx_state = self.env.ref(
            'medical_prescription_state.prescription_order_state_unverified'
        )
        self.assertEqual(rx_orders.mapped('stage_id'), unverified_rx_state)

    def test_post_init_hook_unverified_state_rx_line(self):
        """It should put all Rx line records in unverified state"""
        pre_init_hook(self.cr)
        post_init_hook(self.cr, self.registry)

        rx_lines = self.env['medical.prescription.order.line'].search([])
        unverified_line_state = self.env.ref(
            'medical_prescription_state'
            '.prescription_order_line_state_unverified'
        )
        self.assertEqual(rx_lines.mapped('stage_id'), unverified_line_state)

    def test_post_init_hook_dummy_stages(self):
        """It should remove dummy stages"""
        old_stages = self.env['base.kanban.stage'].search([])
        pre_init_hook(self.cr)
        dummy_stages = self.env['base.kanban.stage'].search([]) - old_stages
        post_init_hook(self.cr, self.registry)

        self.assertFalse(dummy_stages.exists())
