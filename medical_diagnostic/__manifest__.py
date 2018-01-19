# -*- coding: utf-8 -*-
# Copyright 2004-2009 Tiny SPRL
# Copyright 2016-2018 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

{
    'name': 'Medical Diagnostics',
    'summary': 'Support for requesting and recording medical diagnostics',
    'version': '10.0.1.0.0',
    'author': 'LasLabs, Odoo Community Association (OCA)',
    'category': 'Medical',
    'website': 'https://github.com/OCA/vertical-medical',
    'license': 'LGPL-3',
    'installable': True,
    'depends': [
        'medical_pathology',
        'medical_practitioner',
        'medical_procedure',
    ],
    'data': [
        'data/ir_sequence.xml',
        'data/medical_diagnostic_category.xml',
        'security/ir.model.access.csv',
        'views/medical_diagnostic_category.xml',
        'views/medical_diagnostic_criterion.xml',
        'views/medical_diagnostic_observation.xml',
        'views/medical_diagnostic_report.xml',
        'views/medical_diagnostic_request.xml',
        'views/medical_patient.xml',
    ],
    'demo': [
        'demo/medical_patient.xml',
        'demo/medical_diagnostic_request.xml',
        'demo/medical_diagnostic_report.xml',
    ]
}
