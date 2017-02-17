# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import models, api


class ResPartner(models.Model):
    _inherit = ['res.partner', 'medical.abstract.luhn']
    _name = 'res.partner'

    @api.multi
    @api.constrains('country_id', 'ref', 'is_patient')
    def _check_ref(self):
        """ Implement Luhns Formula to validate social security numbers """
        for rec_id in self:
            if rec_id.is_patient and rec_id.ref:
                rec_id._luhn_constrains_helper('ref')
