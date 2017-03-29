# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestMedicalPrescriptionOrderLine(TransactionCase):

    def setUp(self):
        super(TestMedicalPrescriptionOrderLine, self).setUp()
        self.line_model = self.env['medical.prescription.order.line']
        self.advil_1 = self.env.ref(
            'medical_medicament.medical_medicament_advil_1'
        )
        self.patient_1 = self.env.ref(
            'medical.medical_patient_patient_1'
        )
        self.rx_line_1 = self.env.ref(
            'medical_prescription.'
            'medical_prescription_order_order_line_1'
        )
        self.dispense_uom_id = \
            self.rx_line_1.medical_medication_id.medicament_id.uom_id.id

    def test_default_name(self):
        """ Test name added to rx_line as default """
        self.assertTrue(self.rx_line_1.name)

    def test_name_search_medicament_name(self):
        """ Test returns line_ids matching medicament name """
        res = self.line_model.name_search(self.advil_1.name)
        exp = self.line_model.search([(
            'medicament_id.product_id.name',
            'ilike',
            self.advil_1.name,
        )]).name_get()

        res = sorted(set(res))
        exp = sorted(set(exp))
        self.assertEquals(
            res, exp,
        )

    def test_name_search_medicament_strength(self):
        """ Test returns line_ids matching medicament strength """
        res = self.line_model.name_search(self.advil_1.strength)
        exp = self.line_model.search([(
            'medicament_id.strength',
            'ilike',
            self.advil_1.strength,
        )]).name_get()

        res = sorted(set(res))
        exp = sorted(set(exp))
        self.assertEquals(
            res, exp,
        )

    def test_name_search_medicament_uom_name(self):
        """ Test returns line_ids matching medicament strength uom """
        res = self.line_model.name_search(self.advil_1.strength_uom_id.name)
        exp = self.line_model.search([(
            'medicament_id.strength_uom_id.name',
            'ilike',
            self.advil_1.strength_uom_id.name,
        )]).name_get()

        res = sorted(set(res))
        exp = sorted(set(exp))
        self.assertEquals(
            res, exp,
        )

    def test_name_search_medicament_drug_form_code(self):
        """ Test returns line_ids matching medicament drug form code """
        res = self.line_model.name_search(self.advil_1.drug_form_id.code)
        exp = self.line_model.search([(
            'medicament_id.drug_form_id.code',
            'ilike',
            self.advil_1.drug_form_id.code,
        )]).name_get()

        res = sorted(set(res))
        exp = sorted(set(exp))
        self.assertEquals(
            res, exp,
        )

    def test_name_search_patient_name(self):
        """ Test returns line_ids belonging to specified patient """
        res = self.line_model.name_search(self.patient_1.name)
        exp = self.line_model.search([(
            'patient_id.name',
            'ilike',
            self.patient_1.name,
        )]).name_get()

        res = sorted(set(res))
        exp = sorted(set(exp))
        self.assertEquals(
            res, exp,
        )

    def test_name_search_no_params(self):
        """ Test returns all line_ids if blank search params """
        res = self.line_model.name_search()
        exp = self.line_model.search([]).name_get()

        res = sorted(set(res))
        exp = sorted(set(exp))
        self.assertEquals(
            res, exp,
        )

    def test_onchange_medical_medication_id(self):
        '''The medical medicament changes when the medication changes'''
        rx_line2 = self.env.ref(
            'medical_prescription.medical_prescription_order_order_line_5'
        )
        self.rx_line_1.medical_medication_id = rx_line2.medical_medication_id
        self.rx_line_1._onchange_medical_medication_id()
        self.assertEquals(
            self.dispense_uom_id,
            self.rx_line_1.medical_medication_id.medicament_id.uom_id.id,
        )

    def test_default_is_expired(self):
        """Rx line should not be expired if there is no stop date"""
        self.assertEquals(
            self.rx_line_1.is_expired, False
        )

    def test_expired_rx_line(self):
        """Rx line should be expired if stop date has passed"""
        self.rx_line_1.write(
            {'date_stop_treatment': "2000-01-01 12:00:00"}
        )
        self.assertTrue(self.rx_line_1.is_expired)

    def test_not_expired_rx_line(self):
        """Rx line should not be expired if stop date has not passed"""
        self.rx_line_1.write(
            {'date_stop_treatment': "3000-01-01 12:00:00"}
        )
        self.assertEquals(
            self.rx_line_1.is_expired, False
        )
