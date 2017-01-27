# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Medical Prescription Order States",
    "version": "10.0.1.0.0",
    "author": "LasLabs, Odoo Community Association (OCA)",
    "category": "Medical",
    "website": "https://laslabs.com",
    "license": "AGPL-3",
    "post_init_hook": "post_init_hook",
    "depends": [
        "base_kanban_stage",
        "medical_prescription",
    ],
    "data": [
        "views/medical_prescription_order.xml",
        "views/medical_prescription_order_line.xml",
        "data/base_kanban_stage.xml",
    ],
    "installable": True,
    "auto_install": False,
}
