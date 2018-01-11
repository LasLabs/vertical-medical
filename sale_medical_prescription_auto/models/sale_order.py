# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import timedelta
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _sale_order_split(self):
        current_datetime = fields.Datetime.from_string(fields.Datetime.now())

        all_exception_lines = self.env['sale.order.line'].search([
            ('sale_crm_auto_state', '=', 'exception'),
        ])
        all_exception_orders = all_exception_lines.mapped('order_id')

        for order in all_exception_orders:
            hrs_before_split = order.company_id.hrs_before_sale_order_split
            hrs_before_split = timedelta(hours=hrs_before_split)
            split_cutoff = current_datetime - hrs_before_split
            split_cutoff = fields.Datetime.to_string(split_cutoff)

            def _mature(rx_line):
                return rx_line.sale_crm_auto_state_changed <= split_cutoff

            mature_exception_lines = order.order_line.filtered(
                lambda r: r.sale_crm_auto_state == 'exception' and _mature(r)
            )
            mature_confirmed_lines = order.order_line.filtered(
                lambda r: r.sale_crm_auto_state == 'confirmed' and _mature(r)
            )

            if mature_exception_lines and mature_confirmed_lines:
                order.copy({
                    'order_line': [(6, 0, mature_exception_lines.ids)],
                    'origin': order.name,
                })
