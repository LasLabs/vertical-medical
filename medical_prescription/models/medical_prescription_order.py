# -*- coding: utf-8 -*-
# Copyright 2008 Luis Falcon <lfalcon@gnusolidario.org>
# Copyright 2016 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


class MedicalPrescriptionOrder(models.Model):
    _name = 'medical.prescription.order'
    _description = 'Medical Prescription Order'

    name = fields.Char(
        required=True, 
        default=lambda self: _('New'), 
        help='Unique identifier for prescription.'
    )
    patient_id = fields.Many2one(
        comodel_name='medical.patient',
        string='Patient',
        required=True,
        help='Primary patient that this is regarding',
    )
    physician_id = fields.Many2one(
        comodel_name='medical.physician',
        string='Physician',
        required=True,
        help='Physician that issued prescription',
    )
    partner_id = fields.Many2one(
        comodel_name='medical.pharmacy',
        string='Pharmacy',
    )
    prescription_order_line_ids = fields.One2many(
        comodel_name='medical.prescription.order.line',
        inverse_name='prescription_order_id',
        string='Prescription Order Line',
    )
    notes = fields.Text()
    is_pregnancy_warning = fields.Boolean(
        string='Pregnant',
        help='Check this if the primary patient on prescription is pregnant',
    )
    is_verified = fields.Boolean(
        string='Verified',
        help='Check this is the prescription has been confirmed as valid',
    )
    date_prescription = fields.Datetime(
        string='Prescription Date',
        default=lambda s: fields.Datetime.now(),
    )
    active = fields.Boolean(
        compute='_compute_active',
        store=True,
    )
    image = fields.Binary(
        help='Full sized image of the original prescription order.',
        attachment=True,
    )
    image_medium = fields.Binary(
        help='Medium sized image of the original prescription order.',
        compute='_compute_images',
        store=True,
        attachment=True,
    )
    image_small = fields.Binary(
        help='Small sized image of the original prescription order.',
        compute='_compute_images',
        store=True,
        attachment=True,
    )

    @api.multi
    @api.depends('image')
    def _compute_images(self):
        for record in self:
            record.image_medium = tools.image_resize_image_medium(
                record.image,
            )
            record.image_small = tools.image_resize_image_small(
                record.image,
            )

    @api.model
    def create(self, values, check=True):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
        if values.get('name', 'New') == 'New':
            values['name'] = self.env['ir.sequence'].next_by_code('medical.prescription.order') or 'New'
    
        result = super(MedicalPrescriptionOrder, self).create(values)
    
        return result

    @api.multi
    @api.depends('prescription_order_line_ids',
                 'prescription_order_line_ids.active',
                 )
    def _compute_active(self):
        for rec_id in self:
            if not rec_id.prescription_order_line_ids:
                rec_id.active = True
                continue
            rec_id.active = any(
                rec_id.prescription_order_line_ids.mapped('active')
            )

    @api.multi
    def copy(self, default=None):
        '''
        @param self: object pointer
        @param default: dict of default values to be set
        '''
        default = dict(default or {})
        default.update(
            name=('New'),
            )
        return super(MedicalPrescriptionOrder, self).copy(default=default)
