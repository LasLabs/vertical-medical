# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class MedicalPrescriptionOrderLine(models.Model):
    _inherit = 'medical.prescription.order.line'

    sale_order_line_ids = fields.One2many(
        string='Sale Order Lines',
        comodel_name='sale.order.line',
        inverse_name='prescription_order_line_id',
        readonly=True,
    )
    sale_order_ids = fields.Many2many(
        string='Sale Orders',
        comodel_name='sale.order',
        compute='_compute_orders',
        store=True,
        readonly=True,
    )
    receive_date = fields.Datetime(
        default=lambda s: fields.Datetime.now(),
        string='Receive Date',
        help='When the Rx was received',
        related='prescription_order_id.receive_date',
    )

    @api.multi
    @api.depends('sale_order_line_ids')
    def _compute_orders(self):
        for record in self:
            order_ids = []
            for line_id in record.sale_order_line_ids:
                order_ids.append(line_id.order_id.id)
            record.sale_order_ids = self.env['sale.order'].browse(
                set(order_ids)
            )
