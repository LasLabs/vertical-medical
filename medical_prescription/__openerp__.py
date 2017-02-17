# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Medical Prescription',
    'version': '9.0.1.0.0',
    "author": "ACSONE SA/NV, LasLabs, Odoo Community Association (OCA)",
    "maintainer": "ACSONE SA/NV, LasLabs, Odoo Community Association (OCA)",
    "website": "http://www.acsone.eu",
    'category': 'Medical',
    'depends': [
        'medical',
        'medical_medicament',
        'medical_medication',
        'medical_physician',
        'medical_pharmacy',
    ],
    'summary': 'This module introduce the prescription/prescription line'
    'into the medical addons.',
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'views/medical_prescription_order_view.xml',
        'views/medical_prescription_order_line_view.xml',
    ],
    'demo': [
        'demo/medical_prescription_order_demo.xml',
        'demo/medical_prescription_order_line_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
}
