# -*- coding: utf-8 -*-
# Copyright 2004 Tech-Receptives Solutions Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class MedicalFamily(models.Model):
    _name = 'medical.family'
    info = fields.Text(
        string='Extra Information'
    )
    name = fields.Char(
        string='Family',
        required=True
    )
    member_ids = fields.One2many(
        'medical.patient',
        'family_id',
        string='Family Members',
    )
