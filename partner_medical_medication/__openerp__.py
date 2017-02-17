# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Partner Medical Medication',
    'summary': 'Add a medication button to the partner form view',
    'version': '9.0.1.0.0',
    'category': 'Medical',
    'website': 'https://laslabs.com/',
    'author': 'LasLabs',
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'base',
        'medical_medication',
    ],
    'data': [
        'views/res_partner_view.xml',
    ],
}
