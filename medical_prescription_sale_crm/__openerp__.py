# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Medical Prescription Sale CRM',
    'description': 'Create Opportunities from Prescriptions',
    'version': '9.0.1.0.0',
    'author': "LasLabs, Odoo Community Association (OCA)",
    'category': 'Medical',
    'depends': [
        'sale_crm',
        'medical_prescription_sale',
    ],
    "website": "https://laslabs.com",
    "license": "LGPL-3",
    "data": [
        'wizards/medical_lead_wizard_view.xml',
        'views/crm_lead_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
