# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import fields, models


class MedicalMedicament(models.Model):
    _inherit = 'medical.medicament'

    storage = fields.Many2many(
        help='Selection of applicable storage instructions',
        comodel_name='medical.medicament.storage',
    )
