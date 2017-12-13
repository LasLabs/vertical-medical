# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Prescription Verification - States and Logic',
    'summary': 'Introduces prescription verification based on states',
    'version': '10.0.2.0.0',
    'author': 'LasLabs, Odoo Community Association (OCA)',
    'category': 'Medical',
    'website': 'https://laslabs.com',
    'license': 'LGPL-3',
    'installable': True,
    'depends': [
        'medical_prescription_state',
    ],
    'data': [
        'data/base_kanban_stage.xml',
        'views/medical_prescription_order.xml',
    ],
    'demo': [
        'demo/medical_medicament.xml',
        'demo/medical_patient.xml',
        'demo/medical_patient_medication.xml',
        'demo/medical_physician.xml',
        'demo/medical_prescription_order.xml',
        'demo/medical_prescription_order_line.xml',
    ],
    'pre_init_hook': 'pre_init_hook',
}
