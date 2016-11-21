# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class MedicalManufacturer(models.Model):
    _name = 'medical.manufacturer'
    _description = 'Medical Manufacturer'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        required=True,
        ondelete='cascade',
        index=True,
    )

    @api.model
    def create(self, vals):
        vals.update({
            'is_company': True,
            'customer': False,
            'type': self._name,
        })
        return super(MedicalManufacturer, self).create(vals)
