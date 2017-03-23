# -*- coding: utf-8 -*-
# Copyright 2017 Specialty Medical Drugstore LLC
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models

from datetime import datetime, timedelta


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _name = 'sale.order.line'

    state = fields.Selection(
        selection_add=[('confirmed', 'Confirmed'),
                       ('exception', 'Exception'), ]
    )

    @api.model
    def _split_order_line_exceptions(self):
        confirmed = False
        for line in self.order_id.order_line:
            if line.state == 'confirmed':
                confirmed = True
                break
        if confirmed:
            deadline = self.write_date + timedelta(
                hours=self.order_id.hours_until_split
            )
            if deadline > datetime.datetime.now():
                new_order = self.env['sale.order'].create({
                    'order_line': [self],
                })
                self.write({'order_id': new_order})
