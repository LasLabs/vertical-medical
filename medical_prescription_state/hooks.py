# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    """Loaded after installing the module.
    This module's DB modifications will be available.
    :param odoo.sql_db.Cursor cr:
        Database cursor.
    :param odoo.modules.registry.RegistryManager registry:
        Database registry, using v7 api.
    """
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
