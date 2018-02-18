# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class WebsiteConfigSettings(models.TransientModel):

    _inherit = 'website.config.settings'

    default_insurance_product_id = fields.Many2one(
        string='Default Insurance Product',
        comodel_name='product.product',
        related='website_id.default_insurance_product_id',
        required=True,
    )
