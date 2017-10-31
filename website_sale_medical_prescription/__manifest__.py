# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Website Sale Medical Prescription',
    'summary': 'Adds prescription information to website checkout process',
    'version': '10.0.1.1.0',
    'category': 'Website',
    'website': 'https://laslabs.com/',
    'author': 'LasLabs, Odoo Community Association (OCA)',
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'sale_medical_prescription',
        'website_field_autocomplete_related',
        'website_sale',
        'website_sale_medical_medicament',
    ],
    'data': [
        'views/assets.xml',
        'views/medical_prescription_order_template.xml',
        'security/ir.model.access.csv',
        'security/medical_patient_medication_security.xml',
        'security/medical_patient_security.xml',
        'security/medical_pharmacy_security.xml',
        'security/medical_practitioner.xml',
        'security/medical_prescription_order_security.xml',
        'security/res_partner_security.xml',
    ],
}
