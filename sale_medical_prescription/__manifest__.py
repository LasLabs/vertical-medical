# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Medical Prescription Sales',
    'summary': 'Create sale orders from prescriptions',
    'version': '10.0.2.0.0',
    'category': 'Medical',
    'website': 'https://laslabs.com',
    'author': 'LasLabs, Odoo Community Association (OCA)',
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'mail_thread_medical_prescription',
        'medical_pharmacy',
        'sale',
        'stock',
    ],
    'data': [
        'data/product_category_data.xml',
        'views/medical_medicament_view.xml',
        'views/medical_patient_view.xml',
        'views/medical_pharmacy_view.xml',
        'views/medical_practitioner.xml',
        'views/prescription_order_line_view.xml',
        'views/prescription_order_view.xml',
        'views/sale_order_view.xml',
        'wizards/medical_sale_temp_view.xml',
        'wizards/medical_sale_wizard_view.xml',
    ],
    'demo': [
        'demo/product_category_demo.xml',
        'demo/medical_medicament_demo.xml',
        'demo/res_partner.xml',
        'demo/medical_patient_demo.xml',
        'demo/medical_practitioner.xml',
        'demo/medical_patient_medication_demo.xml',
        'demo/medical_pharmacy_demo.xml',
        'demo/medical_prescription_order_demo.xml',
        'demo/medical_prescription_order_line_demo.xml',
        'demo/sale_order_demo.xml',
        'demo/sale_order_line_demo.xml',
    ],
}
