# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    nabp_num = fields.Char(
        help='National Boards of Pharmacy Id #',
    )
    medicaid_num = fields.Char(
        help='Medicaid Id #',
    )
    npi_num = fields.Char(
        help="National Provider Identifier",
    )

    @api.multi
    @api.constrains('npi_num')
    def _check_npi_num(self):
        """ Implement Luhns Formula to validate NPI """
        self._npi_constrains_helper('npi_num')
