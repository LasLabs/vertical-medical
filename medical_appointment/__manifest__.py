# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Medical Appointment - NOT SUPPORTED',
    'summary': 'Not supported! Remove if currently installed.',
    'version': '10.0.2.0.0',
    'author': 'LasLabs, Odoo Community Association (OCA)',
    'category': 'Medical',
    'depends': [
        'auditlog',
        'mail',
        'medical_physician',
    ],
    'data': [
        'views/medical_appointment_view.xml',
        'views/medical_menu.xml',
        'security/ir.model.access.csv',
        'security/medical_security.xml',
        'data/auditlog_rule.xml',
        'data/decimal_precision_data.xml',
        'data/medical_appointment_data.xml',
        'data/medical_appointment_sequence.xml',
    ],
    'website': 'https://laslabs.com',
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_hook_no_install',
}
