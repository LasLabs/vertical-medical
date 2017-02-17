# -*- coding: utf-8 -*-
# © 2015 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import fields, models


class MedicalMedicament(models.Model):
    _inherit = 'medical.medicament'
    medicament_attribute_ids = fields.Many2many(
        string='Attributes',
        comodel_name='medical.medicament.attribute',
        domain=lambda s: "[('medicament_ids', '=', id)]",
    )
