# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class MedicalPrescriptionOrder(models.Model):
    _inherit = 'medical.prescription.order'

    receive_method = fields.Selection(
        string='Receive Method',
        selection=[
            ('online', 'E-Prescription'),
            ('phone', 'Phoned In'),
            ('fax', 'Fax'),
            ('mail', 'Physical Mail'),
            ('transfer', 'Transferred In'),
        ],
        default='fax',
        help='How the Rx was received',
    )
    receive_date = fields.Datetime(
        string='Receive Date',
        default=fields.Datetime.now,
        help='When the Rx was received',
    )
    transfer_pharmacy_id = fields.Many2one(
        string='Transfer Pharmacy',
        comodel_name='medical.pharmacy',
    )
    transfer_direction = fields.Selection(
        string='Transfer Direction',
        selection=[
            ('none', 'None'),
            ('in', 'In'),
            ('out', 'Out'),
        ],
        default='none',
    )
    transfer_ref = fields.Char(
        string='Transfer Reference',
    )
