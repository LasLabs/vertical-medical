# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Medical Website - Prescription Order Lines',
    'version': '9.0.1.0.0',
    'author': "LasLabs, Odoo Community Association (OCA)",
    'category': 'Medical',
    'depends': [
        'website_sale',
        'website_medical_patient',
        'medical_prescription',
        'medical_prescription_sale',
        'medical_prescription_sale_stock',
    ],
    "website": "https://laslabs.com",
    "license": "LGPL-3",
    "data": [
        'views/assets.xml',
        'views/website_medical_template.xml',
        'views/medical_prescription_order_line_template.xml',
        'security/medical_prescription_order_security.xml',
        'security/ir.model.access.csv',
    ],
    "application": False,
    'installable': True,
}
