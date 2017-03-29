# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

import datetime


class MedicalPrescriptionOrderLine(models.Model):
    _name = 'medical.prescription.order.line'
    _description = 'Medical Prescription Order Line'
    _inherit = ['abstract.medical.medication']
    _inherits = {'medical.patient.medication': 'medical_medication_id'}
    _rec_name = 'medical_medication_id'

    prescription_order_id = fields.Many2one(
        comodel_name='medical.prescription.order',
        string='Prescription Order',
        required=True,
    )
    medical_medication_id = fields.Many2one(
        comodel_name='medical.patient.medication',
        string='Medication',
        required=True,
        ondelete='cascade',
    )
    is_substitutable = fields.Boolean()
    qty = fields.Float(
        string='Quantity',
    )
    name = fields.Char(
        required=True,
        default=lambda s: s._default_name(),
    )

    is_expired = fields.Boolean(
        string='Expired?',
        compute='_compute_is_expired',
    )

    @api.model
    def _default_name(self):
        return self.env['ir.sequence'].next_by_code(
            'medical.prescription.order.line'
        )

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):

        args = args or []
        domain = [
            '|', '|', '|', '|',
            ('medicament_id.product_id.name', operator, name),
            ('medicament_id.strength', operator, name),
            ('medicament_id.strength_uom_id.name', operator, name),
            ('medicament_id.drug_form_id.code', operator, name),
            ('patient_id.name', operator, name),
        ]

        recs = self.search(domain + args, limit=limit)
        return recs.name_get()

    @api.onchange('medical_medication_id')
    def _onchange_medical_medication_id(self):
        self.dispense_uom_id = \
            self.medical_medication_id.medicament_id.uom_id.id

    @api.multi
    def _compute_is_expired(self):
        now = datetime.datetime.now()
        for record in self:
            stop = fields.Datetime.from_string(record.date_stop_treatment)
            record.is_expired = stop and stop < now
