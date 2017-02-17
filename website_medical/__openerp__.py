# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Medical Website - Base",
    "summary": "Provides base functionality for medical website.",
    "version": "9.0.1.0.0",
    "category": "Medical",
    "website": "https://laslabs.com",
    "author": "LasLabs, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "medical",
        "website_portal",
        "website_form",
    ],
    "data": [
        "views/assets.xml",
        "views/medical_form_template.xml",
        "views/website_medical_template.xml",
    ],
}
