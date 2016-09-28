# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api, fields


class MedicalPatientDisease(models.Model):
    _inherit = 'medical.patient.disease'

    is_allergy = fields.Boolean(
        string='Allergic Disease',
        store=True,
        compute='_compute_is_allergy',
        help='Check this box to indicate that the disease is an allergy.',
    )

    @api.multi
    @api.depends('pathology_id.code_type_id')
    def _compute_is_allergy(self):
        """ It computes allergy status based on category """
        allergy_code = self.env.ref(
            'medical_patient_disease_allergy.pathology_code_allergy',
        )
        for rec_id in self:
            if rec_id.pathology_id.code_type_id == allergy_code:
                rec_id.is_allergy = True