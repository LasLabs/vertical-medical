# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestMedicalMedicamentGcn(TransactionCase):

    def setUp(self):
        super(TestMedicalMedicamentGcn, self).setUp()
        self.test_gcn = self.env['medical.medicament.gcn'].create({
            'name': '123'
        })

    def test_name_get(self):
        """ It should convert the GCN to the proper format """
        self.assertEquals(self.test_gcn.display_name, '000123')
