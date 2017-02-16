# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class MedicalPatient(models.Model):

    _name = 'medical.patient'
    _inherit = ['medical.patient', 'website.published.mixin', 'mail.thread']

    @api.multi
    def action_invalidate(self):
        return self.write({'active': False})

    @api.multi
    def _compute_website_url(self):
        for record in self:
            record.website_url = "/medical/patients/%s" % (record.id)
