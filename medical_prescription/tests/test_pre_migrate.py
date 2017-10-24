# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

import os
import sys
from psycopg2 import ProgrammingError
from odoo.modules.module import get_module_path
from odoo.tests.common import TransactionCase

module_path = get_module_path('medical_prescription')
migration_path = os.path.join(module_path, 'migrations', '10.0.2.0.0')
sys.path.insert(0, migration_path)
sys.modules.pop('pre-migrate', None)
pre_migrate = __import__('pre-migrate')
migrate = pre_migrate.migrate


class TestPostMigrate(TransactionCase):
    def setUp(self):
        super(TestPostMigrate, self).setUp()

        module = 'medical_prescription'
        test_rx_order_xml_id = module + '.medical_prescription_order_1'
        test_rx_order_2_xml_id = module + '.medical_prescription_order_2'
        self.test_rx_order = self.env.ref(test_rx_order_xml_id)
        self.test_rx_order_2 = self.env.ref(test_rx_order_2_xml_id)
        self.test_rx_set = self.test_rx_order + self.test_rx_order_2

        self.cr.execute(
            """ALTER TABLE medical_prescription_order
            DROP COLUMN practitioner_id"""
        )

    def test_migrate_add_column(self):
        """It should add practitioner_id column to Rx order table"""
        migrate(self.env.cr, None)

        try:
            self.test_rx_order.practitioner_id
        except ProgrammingError as error:
            text = 'medical_prescription_order.practitioner_id does not exist'
            if text in error.pgerror:
                self.fail(
                    'A practitioner_id column was not added to the'
                    ' medical_prescription_order table.'
                )
            else:
                raise

    def test_migrate_associated_physician(self):
        """It should map Rx orders with physicians to right practitioners"""
        test_partner = self.env.ref('base.main_partner')
        test_specialty = self.env.ref(
            'medical_practitioner.medical_specialty_general',
        )
        test_practitioner = self.env['medical.practitioner'].create({
            'name': 'Test Name',
        })
        self.cr.execute(
            """INSERT INTO medical_physician
            (partner_id, specialty_id, equiv_practitioner_id)
            VALUES (%s, %s, %s)
            RETURNING id""",
            (test_partner.id, test_specialty.id, test_practitioner.id),
        )
        test_physician_id = self.cr.fetchone()
        self.test_rx_set.write({'physician_id': test_physician_id})
        migrate(self.env.cr, None)
        resulting_practitioner = self.test_rx_order.practitioner_id
        resulting_practitioner_2 = self.test_rx_order_2.practitioner_id

        self.assertEqual(resulting_practitioner, test_practitioner)
        self.assertEqual(resulting_practitioner_2, test_practitioner)

    def test_migrate_no_associated_physician(self):
        """It should not map Rx orders without physician to a practitioner"""
        migrate(self.env.cr, None)

        result_practitioners = self.test_rx_set.mapped('practitioner_id')
        self.assertFalse(result_practitioners)
