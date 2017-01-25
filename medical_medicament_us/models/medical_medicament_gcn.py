# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class MedicalMedicamentGcn(models.Model):
    _name = 'medical.medicament.gcn'
    _description = 'Medical Medicament GCN'

    name = fields.Char(
        string='GCN',
        help='Generic Code Number - 5 digits',
    )
    medicament_ids = fields.One2many(
        string='Medicament',
        comodel_name='medical.medicament',
        inverse_name='gcn_id',
    )
