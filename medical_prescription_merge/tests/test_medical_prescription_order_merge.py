# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, models
from odoo.exceptions import ValidationError
from odoo.tests.common import SingleTransactionCase


# Add mail.thread to inheritance chains to test logic for handling mail.thread
# fields. This normally happens in mail_thread_medical_prescription

class MedicalPrescriptionOrder(models.Model):
    _name = 'medical.prescription.order'
    _description = 'Medical Prescription Order'
    _inherit = ['medical.prescription.order', 'mail.thread']


class MedicalPrescriptionOrderLine(models.Model):
    _name = 'medical.prescription.order.line'
    _description = 'Medical Prescription Order Line'
    _inherit = ['medical.prescription.order.line', 'mail.thread']


class TestMedicalPrescriptionOrderMerge(SingleTransactionCase):
    @classmethod
    def _init_test_model(cls, model_cls):
        """This builds a model from model_cls in order to test abstract models
        or, in this case, temporarily incorporate the model changes above.
        """
        model_cls._build_model(cls.env.registry, cls.env.cr)
        model = cls.env[model_cls._name].with_context(todo=[])
        model._prepare_setup()
        model._setup_base(partial=False)
        model._setup_fields(partial=False)
        model._setup_complete()
        model._auto_init()
        model.init()
        model._auto_end()

    @classmethod
    def setUpClass(cls):
        super(TestMedicalPrescriptionOrderMerge, cls).setUpClass()
        cls.env.registry.enter_test_mode()
        cls.old_cursor = cls.cr
        cls.cr = cls.registry.cursor()
        cls.env = api.Environment(cls.cr, cls.uid, {})
        cls._init_test_model(MedicalPrescriptionOrder)
        cls._init_test_model(MedicalPrescriptionOrderLine)

    @classmethod
    def tearDownClass(cls):
        cls.env.registry.leave_test_mode()
        cls.cr = cls.old_cursor
        cls.env = api.Environment(cls.cr, cls.uid, {})
        super(TestMedicalPrescriptionOrderMerge, cls).tearDownClass()

    def _new_rx_order(self, extra_values=None):
        base_values = {
            'patient_id': self.env.ref('medical.medical_patient_patient_1').id,
            'practitioner_id': self.env.ref(
                'medical_prescription.medical_practitioner_1'
            ).id,
            'date_prescription': '2016-10-31 23:59:59',
        }
        if extra_values is not None:
            base_values.update(extra_values)

        return self.env['medical.prescription.order'].create(base_values)

    def test_default_merge_orders_wrong_active_model(self):
        '''It should return empty order recordset when active model is wrong'''
        test_wiz = self.env['medical.prescription.order.merge'].with_context(
            active_model=None,
        )

        self.assertFalse(test_wiz._default_merge_orders())
        self.assertEqual(
            test_wiz._default_merge_orders()._name,
            'medical.prescription.order',
        )

    def test_default_merge_orders_no_active_ids(self):
        '''It should return empty order recordset if there are no active IDs'''
        test_wiz = self.env['medical.prescription.order.merge'].with_context(
            active_model='medical.prescription.order',
            active_ids=None,
        )

        self.assertFalse(test_wiz._default_merge_orders())
        self.assertEqual(
            test_wiz._default_merge_orders()._name,
            'medical.prescription.order',
        )

    def test_default_merge_orders_correct_context(self):
        '''It should return order recordset matching the active IDs'''
        test_rx_order_1 = self._new_rx_order()
        test_rx_order_2 = self._new_rx_order()
        test_wiz = self.env['medical.prescription.order.merge'].with_context(
            active_model='medical.prescription.order',
            active_ids=[test_rx_order_1.id, test_rx_order_2.id],
        ).create({})

        self.assertEqual(
            test_wiz._default_merge_orders().ids,
            [test_rx_order_1.id, test_rx_order_2.id],
        )
        self.assertEqual(
            test_wiz._default_merge_orders()._name,
            'medical.prescription.order',
        )

    def test_default_dest_order_wrong_context(self):
        '''It should return empty order recordset if merge default is empty'''
        test_wiz = self.env['medical.prescription.order.merge'].with_context(
            active_model=None,
        )

        self.assertFalse(test_wiz._default_dest_order())
        self.assertEqual(
            test_wiz._default_dest_order()._name,
            'medical.prescription.order',
        )

    def test_default_dest_order_correct_context(self):
        '''It should return first record in merge order default if not empty'''
        test_rx_order_1 = self._new_rx_order()
        test_rx_order_2 = self._new_rx_order()
        test_wiz = self.env['medical.prescription.order.merge'].with_context(
            active_model='medical.prescription.order',
            active_ids=[test_rx_order_1.id, test_rx_order_2.id],
        ).create({})

        self.assertEqual(
            test_wiz._default_dest_order(),
            test_rx_order_1,
        )

    def test_onchange_merge_order_ids_dest_still_valid(self):
        '''It should return dest order domain that reflects new merge orders'''
        test_rx_order_1 = self._new_rx_order()
        test_rx_order_2 = self._new_rx_order()
        test_wiz = self.env['medical.prescription.order.merge'].with_context(
            active_model='medical.prescription.order',
            active_ids=[test_rx_order_1.id, test_rx_order_2.id],
        ).create({})

        self.assertEqual(
            test_wiz._onchange_merge_order_ids()['domain']['dest_order_id'],
            [('id', 'in', [test_rx_order_1.id, test_rx_order_2.id])],
        )

    def test_onchange_merge_order_ids_dest_no_longer_valid(self):
        '''It should clear dest order if it is no longer in merge orders'''
        test_rx_order_1 = self._new_rx_order()
        test_rx_order_2 = self._new_rx_order()
        test_wiz = self.env['medical.prescription.order.merge'].with_context(
            active_model='medical.prescription.order',
            active_ids=[test_rx_order_1.id, test_rx_order_2.id],
        ).new({})
        test_wiz.merge_order_ids = [(3, test_rx_order_1.id, 0)]
        test_wiz._onchange_merge_order_ids()

        self.assertFalse(test_wiz.dest_order_id)

    def test_action_merge_not_enough_orders(self):
        '''It should throw correct error when there are too few merge orders'''
        test_rx_order_1 = self._new_rx_order()
        test_wiz = self.env['medical.prescription.order.merge'].with_context(
            active_model='medical.prescription.order',
            active_ids=[test_rx_order_1.id],
        ).create({})

        with self.assertRaisesRegexp(ValidationError, 'two orders'):
            test_wiz.action_merge()

    def test_action_merge_different_practitioners(self):
        '''It should throw correct error if practitioners are different'''
        test_rx_order_1 = self._new_rx_order()
        test_practitioner_2 = self.env['medical.practitioner'].create({
            'name': 'Test Practitioner 2',
        })
        test_rx_order_2 = self._new_rx_order({
            'practitioner_id': test_practitioner_2.id,
        })
        test_wiz = self.env['medical.prescription.order.merge'].with_context(
            active_model='medical.prescription.order',
            active_ids=[test_rx_order_1.id, test_rx_order_2.id],
        ).create({})

        expected_snippet = 'different practitioners'
        with self.assertRaisesRegexp(ValidationError, expected_snippet):
            test_wiz.action_merge()

    def test_action_merge_different_rx_dates(self):
        '''It should throw correct error when there are different Rx dates'''
        test_rx_order_1 = self._new_rx_order({
            'date_prescription': '2016-10-30 23:59:59',
        })
        test_rx_order_2 = self._new_rx_order()
        test_wiz = self.env['medical.prescription.order.merge'].with_context(
            active_model='medical.prescription.order',
            active_ids=[test_rx_order_1.id, test_rx_order_2.id],
        ).create({})

        with self.assertRaisesRegexp(ValidationError, 'different dates'):
            test_wiz.action_merge()

    def test_action_merge_missing_rx_dates(self):
        '''It should not count missing Rx dates towards error-checking'''
        test_rx_order_1 = self._new_rx_order({
            'date_prescription': None,
        })
        test_rx_order_2 = self._new_rx_order()
        test_wiz = self.env['medical.prescription.order.merge'].with_context(
            active_model='medical.prescription.order',
            active_ids=[test_rx_order_1.id, test_rx_order_2.id],
        ).create({})

        try:
            test_wiz.action_merge()
        except ValidationError:
            self.fail('A ValidationError was raised and should not have been.')

    def test_action_merge_skip_validation_flag(self):
        '''It should skip date/practitioner validations when flag is active'''
        test_rx_order_1 = self._new_rx_order({
            'date_prescription': '2016-10-30 23:59:59',
        })
        test_practitioner_2 = self.env['medical.practitioner'].create({
            'name': 'Test Practitioner 2',
        })
        test_rx_order_2 = self._new_rx_order({
            'practitioner_id': test_practitioner_2.id,
        })
        test_wiz = self.env['medical.prescription.order.merge'].with_context(
            active_model='medical.prescription.order',
            active_ids=[test_rx_order_1.id, test_rx_order_2.id],
        ).create({'skip_validation': True})

        try:
            test_wiz.action_merge()
        except ValidationError as error:
            self.fail(
                'A ValidationError was raised and should not have been.'
                ' It has the following message: %s' % error.args[0]
            )

    def test_action_merge_skip_validation_flag_not_enough_orders(self):
        '''It should not skip order count validation when flag is active'''
        test_rx_order_1 = self._new_rx_order()
        test_wiz = self.env['medical.prescription.order.merge'].with_context(
            active_model='medical.prescription.order',
            active_ids=[test_rx_order_1.id],
        ).create({'skip_validation': True})

        with self.assertRaisesRegexp(ValidationError, 'two orders'):
            test_wiz.action_merge()

    def test_action_merge_no_errors(self):
        '''It should trigger a merge when all validations are successful'''
        test_rx_order_1 = self._new_rx_order()
        test_rx_order_2 = self._new_rx_order()
        test_wiz = self.env['medical.prescription.order.merge'].with_context(
            active_model='medical.prescription.order',
            active_ids=[test_rx_order_1.id, test_rx_order_2.id],
        ).create({})
        test_wiz.action_merge()

        self.assertFalse(test_rx_order_2.exists())

    def test_perform_merge_delete_source_orders(self):
        '''It should always unlink the source orders'''
        test_rx_order_1 = self._new_rx_order()
        test_rx_order_2 = self._new_rx_order()
        test_wiz = self.env['medical.prescription.order.merge']
        test_wiz._perform_merge(test_rx_order_2, test_rx_order_1)

        self.assertFalse(test_rx_order_2.exists())

    def test_perform_merge_x2many_fields(self):
        '''It should combine x2many fields'''
        test_rx_order_1 = self._new_rx_order()
        test_rx_line_1 = self.env['medical.prescription.order.line'].create({
            'prescription_order_id': test_rx_order_1.id,
            'patient_id': self.env.ref('medical.medical_patient_patient_1').id,
            'medicament_id': self.env.ref(
                'medical_medicament.medical_medicament_advil_1'
            ).id,
        })
        test_rx_order_2 = self._new_rx_order()
        test_rx_line_2 = self.env['medical.prescription.order.line'].create({
            'prescription_order_id': test_rx_order_2.id,
            'patient_id': self.env.ref('medical.medical_patient_patient_1').id,
            'medicament_id': self.env.ref(
                'medical_medicament.medical_medicament_advil_1'
            ).id,
        })
        test_rx_line_3 = self.env['medical.prescription.order.line'].create({
            'prescription_order_id': test_rx_order_2.id,
            'patient_id': self.env.ref('medical.medical_patient_patient_1').id,
            'medicament_id': self.env.ref(
                'medical_medicament.medical_medicament_advil_1'
            ).id,
        })
        test_wiz = self.env['medical.prescription.order.merge']
        test_wiz._perform_merge(test_rx_order_2, test_rx_order_1)

        self.assertEqual(
            test_rx_order_1.prescription_order_line_ids.ids,
            [test_rx_line_1.id, test_rx_line_2.id, test_rx_line_3.id],
        )

    def test_perform_merge_many2one_fields(self):
        '''It should properly merge many2one fields'''
        test_rx_order_1 = self._new_rx_order()
        test_pharmacy = self.env['medical.pharmacy'].create({
            'name': 'Test Pharmacy',
        })
        test_rx_order_2 = self._new_rx_order({'partner_id': test_pharmacy.id})
        test_wiz = self.env['medical.prescription.order.merge']
        test_wiz._perform_merge(test_rx_order_2, test_rx_order_1)

        self.assertEqual(test_rx_order_1.partner_id, test_pharmacy)

    def test_perform_merge_many2one_fields_precedence(self):
        '''It should give dest order precedence when merging many2one fields'''
        test_pharmacy_1 = self.env['medical.pharmacy'].create({
            'name': 'Test Pharmacy',
        })
        test_rx_order_1 = self._new_rx_order({
            'partner_id': test_pharmacy_1.id,
        })
        test_pharmacy_2 = self.env['medical.pharmacy'].create({
            'name': 'Test Pharmacy 2',
        })
        test_rx_order_2 = self._new_rx_order({
            'partner_id': test_pharmacy_2.id,
        })
        test_wiz = self.env['medical.prescription.order.merge']
        test_wiz._perform_merge(test_rx_order_2, test_rx_order_1)

        self.assertEqual(test_rx_order_1.partner_id, test_pharmacy_1)

    def test_perform_merge_non_relational_fields(self):
        '''It should properly merge non-relational fields'''
        test_rx_order_1 = self._new_rx_order()
        test_rx_order_2 = self._new_rx_order({'notes': 'Test'})
        test_wiz = self.env['medical.prescription.order.merge']
        test_wiz._perform_merge(test_rx_order_2, test_rx_order_1)

        self.assertEqual(test_rx_order_1.notes, 'Test')

    def test_perform_merge_non_relational_fields_precedence(self):
        '''It should give dest order precedence for non-relational fields'''
        test_rx_order_1 = self._new_rx_order({'notes': 'Precedence'})
        test_rx_order_2 = self._new_rx_order({'notes': 'Test'})
        test_wiz = self.env['medical.prescription.order.merge']
        test_wiz._perform_merge(test_rx_order_2, test_rx_order_1)

        self.assertEqual(test_rx_order_1.notes, 'Precedence')

    def test_perform_merge_message_followers(self):
        """It should properly merge orders with message followers"""
        test_rx_order_1 = self._new_rx_order()
        test_rx_order_2 = self._new_rx_order()
        test_follower_1 = test_rx_order_1.message_follower_ids
        test_rx_order_2.message_follower_ids.unlink()
        test_follower_2 = self.env['mail.followers'].create({
            'res_model': 'medical.prescription.order',
            'res_id': test_rx_order_2.id,
            'partner_id': self.env.ref('base.public_partner').id,
        })
        test_follower_3 = self.env['mail.followers'].create({
            'res_model': 'medical.prescription.order',
            'res_id': test_rx_order_2.id,
            'channel_id': self.env.ref('mail.channel_all_employees').id,
        })
        test_followers = test_follower_1 + test_follower_2 + test_follower_3
        test_wiz = self.env['medical.prescription.order.merge']
        test_wiz._perform_merge(test_rx_order_2, test_rx_order_1)

        self.assertEqual(test_rx_order_1.message_follower_ids, test_followers)

    def test_perform_merge_message_followers_same_partner(self):
        """It should properly merge orders with followers of same partner ID"""
        test_rx_order_1 = self._new_rx_order()
        test_rx_order_2 = self._new_rx_order()
        test_follower_1 = test_rx_order_1.message_follower_ids
        test_follower_2 = test_rx_order_2.message_follower_ids
        test_follower_set = test_follower_1 + test_follower_2
        test_wiz = self.env['medical.prescription.order.merge']
        test_wiz._perform_merge(test_rx_order_2, test_rx_order_1)

        self.assertIn(test_rx_order_1.message_follower_ids, test_follower_set)
        self.assertEqual(len(test_rx_order_1.message_follower_ids), 1)

    def test_perform_merge_message_followers_same_channel(self):
        """It should properly merge orders with followers of same channel ID"""
        test_rx_order_1 = self._new_rx_order()
        test_rx_order_2 = self._new_rx_order()
        test_rx_order_1.message_follower_ids.unlink()
        test_rx_order_2.message_follower_ids.unlink()
        test_channel = self.env.ref('mail.channel_all_employees')
        test_follower_1 = self.env['mail.followers'].create({
            'res_model': 'medical.prescription.order',
            'res_id': test_rx_order_1.id,
            'channel_id': test_channel.id,
        })
        test_follower_2 = self.env['mail.followers'].create({
            'res_model': 'medical.prescription.order',
            'res_id': test_rx_order_2.id,
            'channel_id': test_channel.id,
        })
        test_follower_set = test_follower_1 + test_follower_2
        test_wiz = self.env['medical.prescription.order.merge']
        test_wiz._perform_merge(test_rx_order_2, test_rx_order_1)

        self.assertIn(test_rx_order_1.message_follower_ids, test_follower_set)
        self.assertEqual(len(test_rx_order_1.message_follower_ids), 1)

    def test_perform_merge_message_followers_combine_subtypes(self):
        """It should combine subtypes when merging orders with followers"""
        test_rx_order_1 = self._new_rx_order()
        test_rx_order_2 = self._new_rx_order()
        test_subtype_1 = test_rx_order_1.message_follower_ids.subtype_ids
        test_subtype_2 = self.env.ref('mail.mt_note')
        test_rx_order_2.message_follower_ids.subtype_ids = test_subtype_2
        test_subtypes = test_subtype_1 + test_subtype_2
        test_wiz = self.env['medical.prescription.order.merge']
        test_wiz._perform_merge(test_rx_order_2, test_rx_order_1)

        expected_subtypes = test_rx_order_1.message_follower_ids.subtype_ids
        self.assertEqual(expected_subtypes, test_subtypes)

    def test_perform_merge_messages(self):
        """It should properly merge orders with messages"""
        test_rx_order_1 = self._new_rx_order()
        test_rx_order_2 = self._new_rx_order()
        test_message_1 = test_rx_order_1.message_ids
        test_message_2 = test_rx_order_2.message_ids
        test_messages = test_message_1 + test_message_2
        test_wiz = self.env['medical.prescription.order.merge']
        test_wiz._perform_merge(test_rx_order_2, test_rx_order_1)

        self.assertEqual(test_rx_order_1.message_ids, test_messages)
