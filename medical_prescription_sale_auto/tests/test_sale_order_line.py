# -*- coding: utf-8 -*-
# Copyright 2017 Specialty Medical Drugstore LLC
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestSaleOrderLine(TransactionCase):
    def setUp(self):
        super(TestSaleOrderLine, self).setUp()
        patient = self.env['medical.patient'].create({
            'name': 'Test Patient',
        })
        product_1 = self.env['product.product'].create({
            'name': 'Test Product',
        })
        medicament_1 = self.env['medical.medicament'].create({
            'name': 'Test Medicament',
            'product_id': product_1.id,
            'drug_form_id': 1,
        })
        medication_1 = self.env['medical.patient.medication'].create({
            'medicament_id': medicament_1.id,
            'patient_id': patient.id,
        })
        self.prescription_order = \
            self.env['medical.prescription.order'].create({
                'name': 'Verified Prescription Order',
                'physician_id': 1,
                'patient_id': patient.id,
            })
        self.prescription_order_line_1 = \
            self.env['medical.prescription.order.line'].create({
                'name': 'Rx Order Line 1',
                'quantity': 1.0,
                'medical_medication_id': medication_1.id,
                'patient_id': patient.id,
                'prescription_order_id': self.prescription_order.id,
            })
        product_2 = self.env['product.product'].create({
            'name': 'Test Product 2',
        })
        medicament_2 = self.env['medical.medicament'].create({
            'name': 'Test Medicament 2',
            'product_id': product_2.id,
            'drug_form_id': 1,
        })
        medication_2 = self.env['medical.patient.medication'].create({
            'medicament_id': medicament_2.id,
            'patient_id': patient.id,
        })
        self.prescription_order_line_2 = \
            self.env['medical.prescription.order.line'].create({
                'name': 'Rx Order Line 2',
                'quantity': 1,
                'medical_medication_id': medication_2.id,
                'patient_id': patient.id,
                'prescription_order_id': self.prescription_order.id,
            })
        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'patient_ids': [(6, 0, [patient.id])]
        })
        sale_order = self.env['sale.order'].create({
            'name': 'Test Sale Order',
            'partner_id': partner.id
        })
        self.matching_sale_order_line = self.env['sale.order.line'].create({
            'name': 'Matching Rx Order Line',
            'product_uom_qty': 1.0,
            'product_id': product_1.id,
            'order_partner_id': partner,
            'order_id': sale_order.id,
        })
        self.exception_sale_order_line = self.env['sale.order.line'].create({
            'name': 'Exception Rx Order Line',
            'product_uom_qty': 5000,
            'product_id': product_2.id,
            'order_partner_id': partner.id,
            'order_id': sale_order.id,
        })
        product_3 = self.env['product.product'].create({
            'name': 'Test Product 3',
        })
        medicament_3 = self.env['medical.medicament'].create({
            'name': 'Test Medicament 3',
            'product_id': product_3.id,
            'drug_form_id': 1,
        })
        medication_3 = self.env['medical.patient.medication'].create({
            'medicament_id': medicament_3.id,
            'patient_id': patient.id,
        })
        self.prescription_order_line_3 = \
            self.env['medical.prescription.order.line'].create({
                'name': 'Rx Order Line 3',
                'quantity': 1,
                'medical_medication_id': medication_3.id,
                'patient_id': patient.id,
                'prescription_order_id': self.prescription_order.id,
            })

    def test_sale_order_confirmed(self):
        '''It should mark the sale order line as confirmed
        if it matches the verified prescription line'''
        self.prescription_order.write(
            {'stage_id': 4}
        )
        self.prescription_order.refresh()
        self.prescription_order_line_1.refresh()
        self.matching_sale_order_line.refresh()
        self.assertEquals(
            self.prescription_order_line_1.quantity,
            self.matching_sale_order_line.product_uom_qty
        )
        self.assertEquals(
            self.prescription_order_line_1.
            medical_medication_id.medicament_id.product_id,
            self.matching_sale_order_line.product_id
        )
        self.assertTrue(
            len(
                self.matching_sale_order_line.order_partner_id.patient_ids
            ) > 0
        )
        self.assertTrue(
            self.prescription_order_line_1.patient_id in
            self.matching_sale_order_line.order_partner_id.patient_ids
        )
        self.assertEquals(
            'confirmed',
            self.matching_sale_order_line.state
        )

    def test_sale_order_exception(self):
        '''It should mark the sale order line as an exception if it
        only partially matches the verified prescription line'''
        self.prescription_order.write(
            {'stage_id': 4}
        )
        self.prescription_order.refresh()
        self.prescription_order_line_2.refresh()
        self.exception_sale_order_line.refresh()
        self.assertEquals(
            'exception',
            self.exception_sale_order_line.state
        )

    def test_sale_lead_creation(self):
        '''It should create a new sale lead for a prescription
        line that does not match a sale order line'''
        self.prescription_order.write(
            {'stage_id': 4}
        )
        self.prescription_order.refresh()
        self.prescription_order_line_3.refresh()
        partner_id = self.prescription_order_line_3.\
            prescription_order_id.partner_id.id
        lead = self.env['crm.lead'].search(
            [('partner_id', '=', partner_id)]
        )
        self.assertTrue(lead)
