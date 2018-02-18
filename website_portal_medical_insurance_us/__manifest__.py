# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Medical Website - Insurance",
    "summary": "Adds patient listing and editing to website portal.",
    "version": "10.0.1.0.0",
    "category": "Medical",
    "website": "https://laslabs.com",
    "author": "LasLabs, Odoo Community Association (OCA)",
    "license": "GPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "medical_insurance_us",
        "website_field_autocomplete_related",
        "website_portal_medical_patient",
    ],
    "data": [
        "views/website_medical_template.xml",
        "views/website_config_settings.xml",
        "views/insurance_template.xml",
        "views/assets.xml",
        "data/ir_model_data.xml",
        "security/ir.model.access.csv",
        "security/medical_insurance_company.xml",
        "security/medical_insurance_plan_security.xml",
        "security/medical_insurance_security.xml",
    ],
    "demo": [
        "demo/medical_patient_demo.xml",
        "demo/res_groups_demo.xml",
    ],
}
