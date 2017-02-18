# -*- coding: utf-8 -*-
# Copyright: 2015 LasLabs, Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class MedicalPatient(models.Model):
    _inherit = 'medical.patient'

    role_id = fields.Many2one(
        'medical.family.role',
    )
    family_id = fields.Many2one(
        'medical.family',
    )
    family_member_ids = fields.One2many(
        'medical.patient',
        'family_id',
        string='Family Members',
        related='family_id.member_ids'
    )
