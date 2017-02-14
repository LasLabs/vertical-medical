# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'
    medical_insurance_template_ids = fields.One2many(
        string='Insurance Templates',
        comodel_name='medical.insurance.template',
        compute=lambda s: s._compute_medical_insurance_template_ids()
    )

    @api.multi
    def _compute_medical_insurance_template_ids(self):
        ins_obj = self.env['medical.insurance.template']
        template_ids = ins_obj.search([('pricelist_id', '=', self.id)])
        for template_id in template_ids:
            self.medical_insurance_template_ids += template_id
