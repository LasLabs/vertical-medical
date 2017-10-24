# -*- coding: utf-8 -*-
# Copyright 2015 ACSONE SA/NV
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Medical Prescription',
    'summary': 'Introduces prescription orders and prescription order lines.',
    'version': '10.0.2.0.0',
    'category': 'Medical',
    'website': 'http://www.acsone.eu',
    'author': 'ACSONE SA/NV, LasLabs, Odoo Community Association (OCA)',
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'medical_medication',
        'medical_pharmacy',
    ],
    'data': [
        'data/ir_sequence.xml',
        'security/ir.model.access.csv',
        'views/medical_prescription_order_view.xml',
        'views/medical_prescription_order_line_view.xml',
        'views/medical_menu.xml',
        'views/medical_patient_view.xml',
    ],
    'demo': [
        'demo/res_partner.xml',
        'demo/medical_patient_demo.xml',
        'demo/medical_pharmacy_demo.xml',
        'demo/medical_practitioner.xml',
        'demo/medical_prescription_order_demo.xml',
        'demo/medical_prescription_order_line_demo.xml',
    ],
}
