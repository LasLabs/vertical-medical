# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class MedicalMedicamentGcn(models.Model):
    _name = 'medical.medicament.gcn'
    _description = 'Medical Medicament GCN'

    name = fields.Integer(
        string='GCN',
        help='Generic Code Number - 6 digits',
    )
    medicament_ids = fields.One2many(
        string='Medicament',
        comodel_name='medical.medicament',
        inverse_name='gcn_id',
    )

    @api.multi
    def name_get(self):
        """ Override method to properly display the GCN """
        return [(r.id, '%06d' % r.name) for r in self]
