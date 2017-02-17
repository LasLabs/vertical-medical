# -*- coding: utf-8 -*-
# © 2015 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Medical Medicament Physical Attributes',
    'summary': 'Add abstract physical attributes to medical medicaments.',
    'version': '9.0.1.0.0',
    'author': "LasLabs, Odoo Community Association (OCA)",
    'category': 'Medical',
    'depends': [
        'medical_medicament',
    ],
    "website": "http://github.com/oca/vertical-medical",
    "license": "LGPL-3",
    "data": [
        'views/medical_medicament_view.xml',
        'views/medical_medicament_attribute_view.xml',
        'views/medical_medicament_attribute_type_view.xml',
        'views/medical_menu.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
