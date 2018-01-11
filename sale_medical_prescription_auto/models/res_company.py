# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    hrs_before_sale_order_split = fields.Integer(
        default=48,
        required=True,
    )
