# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Medical Prescription Order State Verification",
    "version": "10.0.1.0.0",
    "author": "LasLabs, Odoo Community Association (OCA)",
    "category": "Medical",
    "website": "https://laslabs.com",
    "license": "AGPL-3",
    "installable": True,
    "auto_install": False,
    "depends": [
        "base_kanban_stage",
        "base_kanban_stage_state",
        "medical_prescription_state",
    ],
}
