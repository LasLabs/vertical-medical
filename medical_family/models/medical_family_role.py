# -*- coding: utf-8 -*-
# Copyright: 2015 LasLabs, Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class MedicalFamilyRole(models.Model):
    _name = 'medical.family.role'
    name = fields.Char(
        size=256,
        string='Role',
        required=True
    )
    dependency = fields.Selection([
        (1, 'Fully Dependent'),
        (5, 'Partially Dependent'),
        (10, 'Self Dependent'),
    ])
