# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{

    'name': 'Medical Appointment',
    'summary': 'Add Appointment concept to medical_physician',
    'version': '9.0.1.0.0',
    'author': 'LasLabs, Odoo Community Association (OCA)',
    'category': 'Medical',
    'depends': [
        'medical_base_history',
        'medical_physician',
    ],
    'data': [
        'views/medical_appointment_view.xml',
        'views/medical_menu.xml',
        'security/ir.model.access.csv',
        'security/medical_security.xml',
        'data/medical_appointment_data.xml',
        'data/medical_appointment_sequence.xml',
    ],
    'website': 'https://laslabs.com',
    'licence': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}
