# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api


class MedicalPhysicianUnavailableWizard(models.TransientModel):
    _name = 'medical.physician.unavailable.wizard'
    _description = 'Medical physicians Unavailable Wizard'

    physician_id = fields.Many2one(
        comodel_name='medical.physician',
        string='Physician',
        required=True,
    )
    date_start = fields.Datetime(
        string='Start',
        default=lambda s: fields.Datetime.now(),
        required=True,
    )
    date_end = fields.Datetime(
        string='End',
        default=lambda s: fields.Datetime.now(),
        required=True,
    )
    institution_id = fields.Many2one(
        comodel_name='res.partner',
        string='Medical Center',
        select=True,
        domain=[('is_institution', '=', True)],
    )

    @api.multi
    def action_set_unavailable(self, cr, uid, ids, context=None):
        if not ids:
            return {}

        appointment_proxy = self.env['medical.appointment']

        this = self.browse(0)
        physician_id = this.physician_id.id
        institution_id = this.institution_id.id
        if institution_id:
            institution_ids = [institution_id]
        else:
            institution_ids = []

        date_start = this.date_start
        date_end = this.date_end

        appointment_proxy._remove_empty_clashes(cr, uid, [], [physician_id],
                                                institution_ids, date_start,
                                                date_end, context=context)
        appointment_proxy._set_clashes_state_to_review(cr, uid, [physician_id],
                                                       institution_ids,
                                                       date_start, date_end,
                                                       context=context)

        return {'type': 'ir.actions.act_window_close'}
