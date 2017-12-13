# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

STATE_MODULE = 'medical_prescription_state'


class MedicalPrescriptionOrder(models.Model):
    _inherit = 'medical.prescription.order'

    verify_method = fields.Selection(
        string='Verification Method',
        selection=[
            ('none', 'Not Provided'),
            ('doctor_phone', 'Called Doctor'),
        ],
        default='none',
        help='Method of Rx verification',
    )
    verify_user_id = fields.Many2one(
        string='Verify User',
        comodel_name='res.users',
        store=True,
        compute='_compute_verified',
        help='User that verified the prescription',
    )
    verify_date = fields.Datetime(
        string='Verification Date',
        store=True,
        compute='_compute_verified',
        help='When the prescription was verified',
    )
    is_verified = fields.Boolean(
        store=True,
        compute='_compute_verified',
        inverse='_inverse_is_verified',
        help='If checked, this prescription has been confirmed as valid',
    )

    @api.multi
    @api.depends('stage_id', 'stage_id.is_verified')
    def _compute_verified(self):
        for record in self:
            if record.stage_id.is_verified:
                record.is_verified = True
                record.verify_user_id = self.env.user
                record.verify_date = fields.Datetime.now()
            else:
                record.is_verified = False
                record.verify_user_id = False
                record.verify_date = False

    @api.multi
    def _inverse_is_verified(self):
        for record in self:
            if record.is_verified and not record.stage_id.is_verified:
                record.stage_id = self.env.ref(
                    STATE_MODULE + '.prescription_order_state_verified'
                )
            elif not record.is_verified and record.stage_id.is_verified:
                record.stage_id = self.env.ref(
                    STATE_MODULE + '.prescription_order_state_exception'
                )

    @api.multi
    def write(self, vals):
        """
        1) Limit changes to verified orders
        2) Move order lines to a hold state when their orders are verified
        3) Move order lines to an exception state when their orders are
        cancelled or marked as exceptions
        """
        cancelled_state = self.env.ref(
            STATE_MODULE + '.prescription_order_state_cancelled'
        )
        exception_state = self.env.ref(
            STATE_MODULE + '.prescription_order_state_exception'
        )
        post_verify_states = cancelled_state + exception_state

        verified_recs = self.filtered(lambda r: r.stage_id.is_verified)
        if verified_recs:
            for key in vals:
                if key not in ('stage_id', 'is_verified', 'verify_method'):
                    raise ValidationError(
                        _('You are trying to edit one or more prescriptions'
                          ' that have already been verified (e.g. %s). Please'
                          ' either cancel them or mark them as exceptions if'
                          ' manual changes are required.')
                        % verified_recs[0].name
                    )

                if key == 'stage_id':
                    stage_model = self.env['base.kanban.stage']
                    stage = stage_model.search([('id', '=', vals[key])])
                    if stage not in post_verify_states:
                        raise ValidationError(
                            _('You are trying to move one or more verified'
                              ' prescriptions into a disallowed state'
                              ' (e.g. %s). Verified prescriptions can only be'
                              ' cancelled or marked as exceptions.')
                            % verified_recs[0].name
                        )

        super_result = super(MedicalPrescriptionOrder, self).write(vals)

        verified_recs_now = self.filtered(lambda r: r.stage_id.is_verified)
        new_verified_recs = verified_recs_now - verified_recs
        line_hold_state = self.env.ref(
            STATE_MODULE + '.prescription_order_line_state_hold'
        )
        new_verified_recs.prescription_order_line_ids.write({
            'stage_id': line_hold_state.id,
        })

        canned_recs = self.filtered(lambda r: r.stage_id in post_verify_states)
        line_exception_state = self.env.ref(
            STATE_MODULE + '.prescription_order_line_state_exception'
        )
        canned_recs.prescription_order_line_ids.write({
            'stage_id': line_exception_state.id,
        })

        return super_result
