# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sale_crm_auto_state = fields.Selection(
        selection=[
            ('unprocessed', 'Not Processed'),
            ('confirmed', 'Confirmed'),
            ('exception', 'Exception'),
        ],
        default='unprocessed',
        index=True,
    )
    sale_crm_auto_state_changed = fields.Datetime(
        compute='_compute_sale_crm_auto_state_changed',
        store=True,
    )

    @api.multi
    @api.depends('sale_crm_auto_state')
    def _compute_sale_crm_auto_state_changed(self):
        for record in self:
            record.sale_crm_auto_state_changed = fields.Datetime.now()
