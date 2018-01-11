# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Medical Prescription Sale Auto',
    'summary': 'Automation triggered by prescription line verification',
    'version': '10.0.1.0.0',
    'category': 'Medical',
    'website': 'https://odoo-community.org/',
    'author': 'LasLabs, Odoo Community Association (OCA)',
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'sale_crm_medical_prescription',
        'sale_stock_medical_prescription',
    ],
    'data': [
        'data/ir_cron.xml',
        'wizards/sale_config_settings.xml',
    ],
    'demo': [
        'demo/medical_medicament.xml',
        'demo/medical_patient.xml',
        'demo/medical_patient_medication.xml',
        'demo/medical_physician.xml',
        'demo/medical_prescription_order.xml',
        'demo/medical_prescription_order_line.xml',
        'demo/sale_order.xml',
        'demo/sale_order_line.xml',
    ],
}
