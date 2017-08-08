# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

{
    "name": "Medical Pathology Import",
    "summary": "This module provides a data import interface for Medical"
               "Pathologies.",
    "version": "10.0.1.0.0",
    "category": "Hidden",
    "website": "https://laslabs.com/",
    "author": "LasLabs, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "depends": [
        "medical_pathology",
    ],
    "data": [
        "wizards/medical_pathology_import.xml",
        "views/medical_menu.xml",
    ],
    "installable": True,
}
