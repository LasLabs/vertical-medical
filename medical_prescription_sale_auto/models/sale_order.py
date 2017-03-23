# -*- coding: utf-8 -*-
# Copyright 2017 Specialty Medical Drugstore LLC
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _name = 'sale.order'

    hours_until_split = fields.Integer(
        string='Hours until Split',
        help='Hours until an order line exception is split into its own order',
        default=48,
    )

    state = fields.Selection(
        selection_add=[('confirmed', 'Confirmed'),
                       ('exception', 'Exception'), ]
    )
