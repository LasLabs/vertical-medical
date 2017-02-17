# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{

    'name': 'Medical Medicament - US Locale',
    'version': '9.0.1.0.0',
    'author': "LasLabs, Odoo Community Association (OCA)",
    'category': 'Medical',
    'depends': [
        'medical_base_us',
        'medical_medication',
    ],
    'website': 'https://laslabs.com',
    'license': 'LGPL-3',
    'data': [
        'views/medical_medicament_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': True,
}
