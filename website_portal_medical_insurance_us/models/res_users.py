# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ResUsers(models.Model):

    _inherit = 'res.users'

    is_medical_insurance = fields.Boolean(
        string='Insurance Customer?',
        default=False,
        help='Use this to activate the experimental insurance workflows.',
    )
