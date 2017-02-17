# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import models


class MedicalPatientWebsiteWizard(models.TransientModel):
    _inherit = 'medical.patient'
    _name = 'medical.patient.website.wizard'
