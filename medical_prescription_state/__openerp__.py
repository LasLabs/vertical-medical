# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Medical Prescription Order States',
    'version': '9.0.1.0.0',
    'author': "LasLabs, Odoo Community Association (OCA)",
    'category': 'Medical',
    'depends': [
        'base_kanban_stage',
        'medical_prescription',
    ],
    'website': 'http://github.com/oca/vertical-medical',
    'license': 'LGPL-3',
    'data': [
        'views/medical_prescription_order.xml',
        'views/medical_prescription_order_line.xml',
    ],
    'installable': True,
    'auto_install': False,
}
