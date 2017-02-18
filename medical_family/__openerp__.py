# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    Medical, HMS Opensource Solution
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Medical Family",
    "summary": "Provides family relations for patients",
    "version": '9.0.1.0.0',
    "category": "Medical",
    "website": "https://laslabs.com",
    "license": "AGPL-3",
    "author": "LasLabs, Odoo Community Association (OCA)",
    "installable": True,
    "auto_install": False,
    "depends": [
        'medical',
    ],
    "data": [
        "views/medical_patient_view.xml",
        "views/medical_family_view.xml",
        "security/ir.model.access.csv",
    ],
}
