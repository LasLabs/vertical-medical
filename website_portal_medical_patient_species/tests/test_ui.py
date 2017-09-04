# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import HttpCase


class TestUi(HttpCase):

    def test_species_patient_form(self):
        """ Should navigate around medical patient views without error """
        code = (
            'odoo.__DEBUG__.services["web_tour.tour"].'
            'run("website_portal_medical_patient_species.'
            'patient_form_species")'
        )
        ready = (
            'odoo.__DEBUG__.services["web_tour.tour"].tours['
            '"website_portal_medical_patient_species.patient_form_species"]'
            '.ready'
        )
        self.phantom_js(
            url_path='/my/medical',
            code=code,
            ready=ready,
            login='portal',
        )
