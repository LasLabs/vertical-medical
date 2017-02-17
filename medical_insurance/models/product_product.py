# -*- coding: utf-8 -*-
# © 2015-TODAY LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'
    is_insurance_plan = fields.Boolean(
        string='Insurance Plan',
        help='Check this if the product is an insurance plan',
    )
