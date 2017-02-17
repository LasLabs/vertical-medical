# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{

    'name': 'Medical Prescription Disease',
    'summary': 'Link the Medical Disease and Prescription Concepts',
    'version': '9.0.1.0.0',
    'author': "LasLabs, Odoo Community Association (OCA)",
    'category': 'Medical',
    'depends': [
        'medical_patient_disease',
        'medical_prescription',
    ],
    'data': [
        'views/medical_prescription_order_line_view.xml',
        'views/medical_patient_disease_view.xml',
    ],
    "website": "https://laslabs.com",
    "license": "LGPL-3",
    'installable': True,
    'auto_install': False,
}
