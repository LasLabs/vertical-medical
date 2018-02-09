# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    @api.constrains('product_id', 'prescription_order_line_id')
    def _check_product(self):
        if self.env.context.get('rx_no_validate'):
            return True
        for record in self:
            try:
                super(SaleOrderLine, self)._check_product()
            except ValidationError:
                gcn = record.prescription_order_line_id.medicament_id.gcn_id
                equivalents = self.env['medical.medicament'].search([
                    ('gcn_id', '=', gcn.id),
                ])
                if record.product_id not in equivalents.mapped('product_id'):
                    raise
