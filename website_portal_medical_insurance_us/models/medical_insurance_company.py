# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class MedicalInsuranceCompany(models.Model):

    _inherit = 'medical.insurance.company'

    is_verified = fields.Boolean(
        help='Check this to indicate that this doctor is a verified entity',
    )
    verified_by_id = fields.Many2one(
        string='Verified By',
        comodel_name='res.users',
        store=True,
        compute='_compute_verified_by_id_and_date',
    )
    verified_date = fields.Datetime(
        store=True,
        compute='_compute_verified_by_id_and_date',
    )

    @api.multi
    @api.depends('is_verified')
    def _compute_verified_by_id_and_date(self):
        for rec_id in self:
            if rec_id.is_verified and not rec_id.verified_date:
                rec_id.verified_by_id = self.env.user.id
                rec_id.verified_date = fields.Datetime.now()
