# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{

    'name': 'Medical Prescription Disease State',
    'summary': 'Adds state and more prescription context to disease concept',
    'version': '10.0.1.0.0',
    'author': "LasLabs, Odoo Community Association (OCA)",
    'category': 'Medical',
    'depends': [
        'medical_prescription_disease',
    ],
    'data': [
        'views/medical_patient_disease_view.xml',
    ],
    "website": "https://laslabs.com",
    "license": "LGPL-3",
    'installable': False,
    'auto_install': False,
}
