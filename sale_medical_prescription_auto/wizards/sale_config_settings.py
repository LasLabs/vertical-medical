# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class SaleConfigSettings(models.TransientModel):
    _inherit = 'sale.config.settings'

    hrs_before_sale_order_split = fields.Integer(
        related='company_id.hrs_before_sale_order_split',
        string='Hours Before Sale Order Split',
        help='This field determines the minimum number of hours that must pass'
             ' before a medical sale order with invalid order lines will be'
             ' automatically split to isolate the invalid lines.',
    )
