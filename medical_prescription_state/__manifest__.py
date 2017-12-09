# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Medical Prescription State',
    'version': '10.0.2.0.0',
    'author': 'LasLabs, Odoo Community Association (OCA)',
    'category': 'Medical',
    'website': 'https://laslabs.com',
    'license': 'LGPL-3',
    'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',
    'depends': [
        'base_kanban_stage',
        'medical_prescription',
    ],
    'data': [
        'data/base_kanban_stage.xml',
        'views/medical_prescription_order.xml',
        'views/medical_prescription_order_line.xml',
    ],
    'installable': True,
}
