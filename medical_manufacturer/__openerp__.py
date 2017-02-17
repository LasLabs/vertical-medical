# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{

    'name': 'Medical Manufacturer',
    'summary': 'This module adds the concept of a manufacturer on products.',
    'version': '9.0.1.0.0',
    'author': "LasLabs, Odoo Community Association (OCA)",
    'category': 'Medical',
    "website": "https://laslabs.com",
    "license": "LGPL-3",
    'depends': [
        'medical_medicament',
    ],
    'data': [
        'views/medical_manufacturer_view.xml',
        'views/medical_menu.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
