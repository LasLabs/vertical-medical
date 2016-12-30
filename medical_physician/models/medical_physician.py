# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class MedicalPhysician(models.Model):
    _name = 'medical.physician'
    _inherits = {'res.users': 'user_id'}
    _description = 'Medical Physicians'
    _sql_constraints = [
        ('user_id_uniq', 'UNIQUE(user_id)',
         'Cannot relate two physicians to the same user.'),
    ]

    user_id = fields.Many2one(
        string='Related User',
        comodel_name='res.users',
        required=True,
        ondelete='cascade',
    )
    code = fields.Char(
        string='ID',
        help='Physician Code',
    )
    specialty_id = fields.Many2one(
        help='Specialty Code',
        comodel_name='medical.specialty',
        default=lambda self: self.env.ref(
            'medical_physician.medical_specialty_gp',
        ),
        required=True,
    )
    medical_center_primary_id = fields.Many2one(
        string='Primary Medical Center',
    )
    medical_center_secondary_ids = fields.Many2many(
        string='Secondary Medical Centers',
    )

    @api.model
    def create(self, vals):
        vals.update({
            'customer': False,
            'type': self._name,
        })
        if not vals.get('code'):
            sequence = self.env['ir.sequence'].next_by_code(
                self._name,
            )
            vals['code'] = sequence
        return super(MedicalPhysician, self).create(vals)

    @api.model_cr_context
    def get_by_user(self, user):
        """ It returns the physician that is bound to user, if any """
        return self.search([('user_id', '=', user.id)])
