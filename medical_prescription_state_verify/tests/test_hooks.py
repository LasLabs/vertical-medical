# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.tests.common import TransactionCase
from ..hooks import pre_init_hook


class TestHooks(TransactionCase):
    def _check_for_column(self, column_name):
        self.cr.execute(
            """SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'medical_prescription_order'
            AND column_name = %s""",
            [column_name],
        )

        return bool(self.cr.fetchone())

    def setUp(self):
        super(TestHooks, self).setUp()

        self.cr.execute(
            """ALTER TABLE medical_prescription_order
            DROP COLUMN is_verified_old"""
        )

    def test_pre_init_hook_is_verified(self):
        """It should rename is_verified column if present"""
        pre_init_hook(self.cr)

        self.assertFalse(self._check_for_column('is_verified'))
        self.assertTrue(self._check_for_column('is_verified_old'))

    def test_pre_init_hook_verify_date(self):
        """It should rename verify_date column if present"""
        pre_init_hook(self.cr)

        self.assertFalse(self._check_for_column('verify_date'))
        self.assertTrue(self._check_for_column('verify_date_old'))

    def test_pre_init_hook_verify_method(self):
        """It should rename verify_method column if present"""
        pre_init_hook(self.cr)

        self.assertFalse(self._check_for_column('verify_method'))
        self.assertTrue(self._check_for_column('verify_method_old'))

    def test_pre_init_hook_verify_user_id(self):
        """It should rename verify_user_id column if present"""
        pre_init_hook(self.cr)

        self.assertFalse(self._check_for_column('verify_user_id'))
        self.assertTrue(self._check_for_column('verify_user_id_old'))
