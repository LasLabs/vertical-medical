# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_medicament = fields.Boolean(
        readonly=True,
        help=_('Check if the product is a medicament'),
    )
    is_vaccine = fields.Boolean(
        string='Vaccine',
        help=_('Check if the product is a vaccine'),
    )
