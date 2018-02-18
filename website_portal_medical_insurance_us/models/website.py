# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class Website(models.Model):

    _inherit = 'website'

    default_insurance_product_id = fields.Many2one(
        string='Default Insurance Product',
        comodel_name='product.product',
    )
