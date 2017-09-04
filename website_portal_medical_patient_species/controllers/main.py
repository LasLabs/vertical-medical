# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.http import request

from odoo.addons.website_portal_medical_patient.controllers.main import (
    WebsiteMedical
)


class WebsiteMedical(WebsiteMedical):

    def _inject_medical_detail_vals(self, patient_id=0, **kwargs):
        vals = super(WebsiteMedical, self)._inject_medical_detail_vals(
            patient_id,
            **kwargs
        )
        species_ids = request.env['medical.patient.species'].search([])
        vals.update({
            'species': species_ids,
        })
        return vals
