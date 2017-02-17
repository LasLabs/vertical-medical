# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp.tests.common import TransactionCase


class TestMedicalManufacturer(TransactionCase):

    def setUp(self,):
        super(TestMedicalManufacturer, self).setUp()
        self.model_obj = self.env['medical.manufacturer']
        self.vals = {
            'name': 'Test Pharm',
        }

    def _new_record(self, ):
        return self.model_obj.create(self.vals)

    def test_is_manufacturer(self, ):
        ''' Validate is_manufacturer is set on partner '''
        rec_id = self._new_record()
        self.assertTrue(rec_id.is_manufacturer)
