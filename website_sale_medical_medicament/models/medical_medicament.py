# -*- coding: utf-8 -*-
# © 2016-TODAY LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import models, api


class MedicalMedicament(models.Model):
    _inherit = 'medical.medicament'

    @api.multi
    def website_publish_button(self):
        for rec_id in self:
            rec_id.product_tmpl_id.website_publish_button()
        return True

    @api.multi
    def open_website_url(self):
        self.ensure_one()
        return self.product_tmpl_id.open_website_url()
