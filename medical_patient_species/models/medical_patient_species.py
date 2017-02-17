# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning


class MedicalPatientSpecies(models.Model):
    _name = 'medical.patient.species'
    _description = 'Medical Patient Species'

    name = fields.Char(
        string='Species',
        help='Name of the species',
        size=256,
        required=True,
        translate=True,
    )
    is_person = fields.Boolean(
        readonly=True,
        default=False,
    )

    @api.multi
    def unlink(self):
        for record in self:
            if record.id == self.env.ref('medical_patient_species.human').id:
                raise Warning(
                    _('Human is a permanent record and cannot be destroyed')
                )
            else:
                return super(MedicalPatientSpecies, record).unlink()

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),
    ]
