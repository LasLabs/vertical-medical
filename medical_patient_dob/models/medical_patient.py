# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MedicalPatient(models.Model):
    _inherit = 'medical.patient'

    @api.multi
    def _format_birthdate_date(self):
        self.ensure_one()
        date = 'No DoB'
        if self.birthdate_date:
            date = fields.Datetime.from_string(self.birthdate_date).strftime(
                '%m/%d/%Y'
            )
        return ' [%s]' % date

    @api.multi
    def name_get(self):
        res = []
        for rec_id in self:
            name = '%s%s' % (rec_id.name, rec_id._format_birthdate_date())
            res.append((rec_id.id, name))
        return res
