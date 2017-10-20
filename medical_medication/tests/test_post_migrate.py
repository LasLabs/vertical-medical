# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

import os
import sys
from odoo.modules.module import get_module_path
from odoo.tests.common import TransactionCase

module_path = get_module_path('medical_medication')
migration_path = os.path.join(module_path, 'migrations', '10.0.2.0.0')
sys.path.insert(0, migration_path)
sys.modules.pop('post-migrate', None)
post_migrate = __import__('post-migrate')
migrate = post_migrate.migrate


class TestPostMigrate(TransactionCase):
    def setUp(self):
        super(TestPostMigrate, self).setUp()

        module = 'medical_medication'
        test_medication_xml_id = module + '.medical_patient_medication_1'
        test_medication_2_xml_id = module + '.medical_patient_medication_2'
        self.test_medication = self.env.ref(test_medication_xml_id)
        self.test_medication_2 = self.env.ref(test_medication_2_xml_id)
        self.test_med_set = self.test_medication + self.test_medication_2

    def test_migrate_associated_physician(self):
        """It should map medications with physicians to right practitioners"""
        test_partner = self.env.ref('base.main_partner')
        test_specialty = self.env.ref(
            'medical_practitioner.medical_specialty_general',
        )
        test_practitioner = self.env['medical.practitioner'].create({
            'name': 'Test Name',
        })
        self.cr.execute(
            'INSERT INTO medical_physician'
            '(partner_id, specialty_id, equiv_practitioner_id)'
            'VALUES (%s, %s, %s)'
            'RETURNING id',
            (test_partner.id, test_specialty.id, test_practitioner.id),
        )
        test_physician_id = self.cr.fetchone()
        self.test_med_set.write({'physician_id': test_physician_id})
        migrate(self.env.cr, None)
        resulting_practitioner = self.test_medication.practitioner_id
        resulting_practitioner_2 = self.test_medication_2.practitioner_id

        self.assertEqual(resulting_practitioner, test_practitioner)
        self.assertEqual(resulting_practitioner_2, test_practitioner)

    def test_migrate_no_associated_physician(self):
        """It should not map medications without physician to a practitioner"""
        migrate(self.env.cr, None)

        result_practitioners = self.test_med_set.mapped('practitioner_id')
        self.assertFalse(result_practitioners)
