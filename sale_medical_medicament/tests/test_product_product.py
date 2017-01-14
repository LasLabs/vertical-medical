# -*- coding: utf-8 -*-
# © 2016-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestProductProduct(TransactionCase):

    def setUp(self):
        super(TestProductProduct, self).setUp()
        self.advil = self.env.ref(
            'medical_medicament.medical_medicament_advil_1_product_product'
        )

    def test_name_get(self):
        self.assertEqual(
            self.advil.display_name,
            'Advil 0.2 g - CAP,
        )
