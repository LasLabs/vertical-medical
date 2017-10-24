# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import mock

from odoo.tests.common import TransactionCase


MODEL = 'odoo.addons.medical_prescription.models.medical_prescription_order'


class TestMedicalPrescriptionOrder(TransactionCase):

    def setUp(self):
        super(TestMedicalPrescriptionOrder, self).setUp()
        self.rx_1 = self.env.ref(
            'medical_prescription.medical_prescription_order_1',
        )
        self.rx_6 = self.env.ref(
            'medical_prescription.medical_prescription_order_6',
        )

    def test_sequence_for_name(self):
        """ Test name created if there is none """
        self.assertTrue(
            self.rx_1.name,
        )

    def test_compute_active(self):
        """ Test active is True if rx line_ids present """
        self.assertTrue(
            self.rx_1.active,
        )

    def test_compute_active_no_line_ids(self):
        """ Test active is True if no rx line_ids """
        self.assertTrue(
            self.rx_6.active,
        )

    def test_compute_active_false(self):
        """ It should set active to false when lines are deactivated """
        self.rx_1.prescription_order_line_ids.write({
            'active': False,
        })
        self.assertFalse(
            self.rx_1.active,
        )

    @mock.patch('%s.tools' % MODEL)
    def test_compute_images_small(self, tools):
        """It should write the scaled down images to the record."""
        image = 'image'.encode('base64')
        image_small = 'test-small'.encode('base64')
        image_medium = 'test-medium'.encode('base64')
        tools.image_resize_image_small.return_value = image_small
        tools.image_resize_image_medium.return_value = image_medium
        self.rx_1.write({'image': image})
        tools.image_resize_image_small.assert_called_once_with(image)
        self.assertEqual(
            self.rx_1.image_small,
            image_small,
        )

    @mock.patch('%s.tools' % MODEL)
    def test_compute_images_medium(self, tools):
        """It should write the scaled down images to the record."""
        image = 'image'.encode('base64')
        image_small = 'test-small'.encode('base64')
        image_medium = 'test-medium'.encode('base64')
        tools.image_resize_image_small.return_value = image_small
        tools.image_resize_image_medium.return_value = image_medium
        self.rx_1.write({'image': image})
        tools.image_resize_image_medium.assert_called_once_with(image)
        self.assertEqual(
            self.rx_1.image_medium,
            image_medium,
        )
