# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class MedicalPhysician(models.Model):
    _name = 'medical.physician'
    _inherit = 'medical.abstract.entity'
    _description = 'Medical Physician (DEPRECATED)'

    code = fields.Char(
        string='ID',
        help='Physician Code',
    )
    specialty_id = fields.Many2one(
        help='Specialty Code',
        comodel_name='medical.specialty',
        default=lambda self: self.env.ref(
            'medical_practitioner.medical_specialty_general',
        ),
        required=True,
    )
    info = fields.Text(
        string='Extra info',
        help='Extra Info',
    )
    active = fields.Boolean(
        help='If unchecked, it will allow you to hide the physician without '
             'removing it.',
        default=True,
    )
    equiv_practitioner_id = fields.Many2one(
        comodel_name='medical.practitioner',
    )

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        """Overload to prevent creation of new physicians"""
        raise DeprecationWarning(
            'You are trying to create a record using the deprecated model'
            ' medical.physician, which will be removed in v11. Please create a'
            ' medical.practitioner record instead.'
        )

    @api.multi
    def write(self, vals):
        """Overload to log error when physicians are modified"""
        _logger.error(
            'You are writing to the deprecated model medical.physician, which'
            ' will be removed in v11. Please modify the equivalent'
            ' medical.practitioner record instead. This can be found via the'
            ' equiv_practitioner_id field.'
        )

        result = super(MedicalPhysician, self).write(vals)
        return result
