# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from mock import Mock
import os
import sys
from odoo.modules.module import get_module_path
from odoo.tests.common import TransactionCase

module_path = get_module_path('medical_prescription_state_verify')
migration_path = os.path.join(module_path, 'migrations', '10.0.2.0.0')
sys.path.insert(0, migration_path)
sys.modules.pop('pre-migrate', None)
pre_migrate = __import__('pre-migrate')
migrate = pre_migrate.migrate
hook_mock = pre_migrate.pre_init_hook = Mock()


class TestPreMigrate(TransactionCase):
    def test_migrate_hook_call(self):
        """It should correctly call pre_init_hook"""
        migrate(self.cr, None)

        hook_mock.assert_called_once_with(self.cr)
