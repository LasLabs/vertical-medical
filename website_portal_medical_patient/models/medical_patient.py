# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

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

    @api.model
    def _search_related_patients(self):
        """ Search patients current user is legal rep of """
        partner_id = self.env.user.partner_id
        return self.env['medical.patient'].search([
            '|',
            ('partner_id', '=', partner_id.id),
            ('parent_id', '=', partner_id.id),
        ])
