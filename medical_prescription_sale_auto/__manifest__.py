# -*- coding: utf-8 -*-
# Copyright 2017 Specialty Medical Drugstore LLC
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Medical Prescription Sale Auto",
    "summary": "Matches prescription order line with sale order line",
    "version": "10.0.1.0.0",
    "category": "Medical",
    "website": "https://odoo-community.org/",
    "author": "SMDrugstore, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
        "sale",
        "medical_prescription_state",
        "medical_prescription_state_verify",
    ],
    "data": [
        "views/sale_order_view.xml",
    ],
}
