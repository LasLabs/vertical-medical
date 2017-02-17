# -*- coding: utf-8 -*-
# © 2016-TODAY LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import models


class MedicalPatientWebsiteWizard(models.TransientModel):
    _inherit = 'medical.patient'
    _name = 'medical.patient.website.wizard'
