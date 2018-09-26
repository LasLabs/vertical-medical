# -*- coding: utf-8 -*-
# Copyright 2008 Luis Falcon <lfalcon@gnusolidario.org>
# © 2016 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from odoo.modules import get_module_resource


class MedicalPhysician(models.Model):
    _name = 'medical.physician'
    _inherit = 'medical.abstract.entity'
    _description = 'Medical Physicians'

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
    info = fields.Text(
        string='Extra info',
        help='Extra Info',
    )
    active = fields.Boolean(
        help='If unchecked, it will allow you to hide the physician without '
             'removing it.',
        default=True,
    )
    # schedule_template_ids = fields.One2many(
    #     string='Related schedules',
    #     help='Schedule template of the physician',
    #     comodel_name='medical.physician.schedule.template',
    #     inverse_name='physician_id',
    # )

    @api.model
    def _create_vals(self, vals):
        vals['customer'] = False
        if not vals.get('code'):
            sequence = self.env['ir.sequence'].sudo().next_by_code(
                self._name,
            )
            vals['code'] = sequence
        return super(MedicalPhysician, self)._create_vals(vals)

    @api.model
    def _get_default_image_path(self, vals):
        super(MedicalPhysician, self)._get_default_image_path(vals)
        img_path = 'physician-%s-avatar.png' % vals.get('gender')
        img_path = get_module_resource(
            'medical_pharmacy', 'static/src/img', img_path,
        )
        if not img_path:
            img_path = get_module_resource(
                'medical_physician',
                'static/src/img',
                'physician-male-avatar.png',
            )
        return img_path
