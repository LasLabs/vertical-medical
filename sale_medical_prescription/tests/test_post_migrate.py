# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

import os
import sys
from odoo.modules.module import get_module_path
from odoo.tests.common import TransactionCase

module_path = get_module_path('sale_medical_prescription')
migration_path = os.path.join(module_path, 'migrations', '10.0.2.0.0')
sys.path.insert(0, migration_path)
sys.modules.pop('post-migrate', None)
post_migrate = __import__('post-migrate')
migrate = post_migrate.migrate


class TestPostMigrate(TransactionCase):
    def test_migrate_correct_update(self):
        """It should update new practitioner fields based on physician data"""
        test_partner = self.env.ref('base.main_partner')
        test_specialty = self.env.ref(
            'medical_practitioner.medical_specialty_general',
        )
        test_practitioner = self.env['medical.practitioner'].create({
            'name': 'Test Name',
        })
        test_user = self.env.ref('base.default_user')
        test_date = '2017-10-25 00:01:01'
        self.cr.execute(
            """INSERT INTO medical_physician
            (partner_id, specialty_id, equiv_practitioner_id,
            is_verified, verified_by_id, verified_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id""",
            (test_partner.id, test_specialty.id, test_practitioner.id, True,
             test_user.id, test_date),
        )
        migrate(self.env.cr, None)

        self.assertTrue(test_practitioner.is_verified)
        self.assertEqual(test_practitioner.verified_by_id, test_user)
        self.assertEqual(test_practitioner.verified_date, test_date)
