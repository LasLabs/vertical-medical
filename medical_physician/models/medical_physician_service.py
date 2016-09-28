# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models
from openerp.addons.medical.medical_constants import minutes


class MedicalPhysicianService(models.Model):
    _name = 'medical.physician.service'
    _inherits = {'product.product': 'product_id'}
    _description = 'Medical Physicians Services'

    product_id = fields.Many2one(
        string='Related Product',
        help='Product-related information for appointment type',
        comodel_name='product.product',
        required=True,
        ondelete='restrict',
    )
    physician_id = fields.Many2one(
        string='Physician',
        help='The physician for the appointment',
        comodel_name='medical.physician',
        required=True,
        select=True,
        ondelete='cascade',
    )
    service_duration = fields.Selection(
        selection=minutes,
        string='Duration',
        help='Duration of the appointment in minutes',
    )
