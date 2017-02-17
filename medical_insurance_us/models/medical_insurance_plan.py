# -*- coding: utf-8 -*-
# © 2015-TODAY LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import fields, models


class MedicalInsurancePlan(models.Model):
    _inherit = 'medical.insurance.plan'
    person_num = fields.Integer('Person Number')
