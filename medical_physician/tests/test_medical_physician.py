# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from mock import patch
from odoo.tests.common import TransactionCase

LOGGER_PATH = 'odoo.addons.medical_physician.models.medical_physician._logger'


class TestMedicalPhysician(TransactionCase):
    def setUp(self):
        super(TestMedicalPhysician, self).setUp()

        self.test_physician = self.env['medical.physician'].new({})

    def test_create_raise_deprecation_exception(self):
        """It should raise correct deprecation exception"""
        with self.assertRaises(DeprecationWarning):
            self.test_physician.create({})

    def test_create_disabled(self):
        """It should not create a new record"""
        self.test_physician.search([]).unlink()
        try:
            self.test_physician.create({})
        except DeprecationWarning:
            pass

        expected_records = self.test_physician.search([])
        self.assertFalse(expected_records)

    @patch(LOGGER_PATH)
    def test_write_log_error(self, logger_mock):
        """It should log error with deprecation message"""
        self.test_physician.write({'name': 'Test Name'})

        logger_mock.error.assert_called_once()
        self.assertIn('deprecated model', logger_mock.error.call_args[0][0])

    @patch('odoo.models.BaseModel.write')
    @patch(LOGGER_PATH)
    def test_write_parent_call_and_return(self, logger_mock, write_mock):
        """It should correctly call parent write method and return result"""
        write_mock.return_value = test_value = 'Test Value'
        test_vals = {'name': 'Test Name'}
        result = self.test_physician.write(test_vals)

        write_mock.assert_called_once_with(test_vals)
        self.assertEqual(result, test_value)
