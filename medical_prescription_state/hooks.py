# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, SUPERUSER_ID


def pre_init_hook(cr):
    """Create dummy default stages so that stage_id can be populated as needed,
    allowing NOT NULL constraint to be added during install
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    with cr.savepoint():
        rx_model_record = env['ir.model'].search([
            ('model', '=', 'medical.prescription.order'),
        ])
        env['base.kanban.stage'].create({
            'name': 'Dummy Stage',
            'res_model_id': rx_model_record.id,
        })
        rx_line_model_record = env['ir.model'].search([
            ('model', '=', 'medical.prescription.order.line'),
        ])
        env['base.kanban.stage'].create({
            'name': 'Dummy Stage',
            'res_model_id': rx_line_model_record.id,
        })


def post_init_hook(cr, registry):
    """Replace dummy data with correct default stages and clean up"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    with cr.savepoint():
        rx_state = env.ref(
            'medical_prescription_state.prescription_order_state_unverified',
        )
        line_state = env.ref(
            'medical_prescription_state.'
            'prescription_order_line_state_unverified',
        )
        env['medical.prescription.order'].search([]).write({
            'stage_id': rx_state.id,
        })
        env['medical.prescription.order.line'].search([]).write({
            'stage_id': line_state.id,
        })

        rx_model_names = (
            'medical.prescription.order',
            'medical.prescription.order.line',
        )
        env['base.kanban.stage'].search([
            ('name', '=', 'Dummy Stage'),
            ('res_model_id.model', 'in', rx_model_names),
        ]).unlink()
