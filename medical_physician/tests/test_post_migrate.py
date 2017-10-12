# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from mock import patch, Mock
import os
import sys
from odoo.modules.module import get_module_path
from odoo.tests.common import TransactionCase

module_path = get_module_path('medical_physician')
migration_path = os.path.join(module_path, 'migrations', '10.0.2.0.0')
sys.path.insert(0, migration_path)
sys.modules.pop('post-migrate', None)
post_migrate = __import__('post-migrate')
migrate = post_migrate.migrate
_practitioner_from_physician = post_migrate._practitioner_from_physician

MODEL_PATH = 'odoo.addons.medical_physician.models.medical_physician'
SEARCH_PATH = MODEL_PATH + '.MedicalPhysician.search'
COPY_DATA_PATH = MODEL_PATH + '.MedicalPhysician.copy_data'
IR_MODEL_PATH = 'odoo.addons.base.ir.ir_model'
IR_SEARCH_PATH = IR_MODEL_PATH + '.IrModel.search'
HELPER_PATH = IR_MODEL_PATH + '.IrModelFields._prepare_update'


class TestPostMigrate(TransactionCase):
    def setUp(self):
        super(TestPostMigrate, self).setUp()

        test_specialty_name = 'medical_practitioner.medical_specialty_general'
        self.test_old_specialty = self.env.ref(test_specialty_name)
        self.test_partner = self.env.ref('base.main_partner')

        physician_model = self.env['medical.physician']
        physician_model.search([]).unlink()
        self.test_physician_data = {
            'code': 'Test Code',
            'specialty_id': self.test_old_specialty.id,
            'info': 'Test Info',
            'active': True,
            'schedule_template_ids': False,
            'equiv_practitioner_id': False,
        }
        self.test_physician = physician_model.new(self.test_physician_data)
        self.test_physician.partner_id = self.test_partner
        self.test_physician_2 = physician_model.new({})
        self.test_physician_set = self.test_physician + self.test_physician_2

        old_ref = self.env.ref

        def ref_mock_logic(xml_id):
            if xml_id == 'medical_physician.medical_specialty_gp':
                return self.test_old_specialty
            else:
                return old_ref(xml_id)
        self.env.ref = Mock(side_effect=ref_mock_logic)

        self.test_model_record = self.env['ir.model'].create({
            'name': 'Test Model Record',
            'model': 'test.model',
            'state': 'base',
        })
        self.test_model_record_2 = self.env['ir.model'].create({
            'name': 'Test Model Record',
            'model': 'test.model.2',
            'state': 'base',
        })
        self.test_model_set = self.test_model_record + self.test_model_record_2

        self.removed = [
            'medical.physician.schedule.template',
            'medical.physician.service',
            'medical.physician.unavailable.wizard',
        ]

    @patch(MODEL_PATH + '.MedicalPhysician.write', autospec=True)
    @patch(SEARCH_PATH)
    def test_migrate_update_physician_specialty(self, search_mock, write_mock):
        """It should update physicians with old GP specialty to use new one"""
        search_mock.return_value = self.test_physician_set
        post_migrate._practitioner_from_physician = Mock()
        migrate(self.env.cr, None)

        new_gp = self.env.ref('medical_practitioner.medical_specialty_gp')
        expected_args = {'specialty_id': new_gp.id}
        write_mock.assert_called_once_with(self.test_physician, expected_args)

    @patch(SEARCH_PATH)
    def test_migrate_call_practitioner_helper(self, search_mock):
        """It should call practitioner creation helper once per physician"""
        search_mock.return_value = self.test_physician_set
        post_migrate._practitioner_from_physician = Mock()
        migrate(self.env.cr, None)
        resulting_calls = post_migrate._practitioner_from_physician.mock_calls

        self.assertEqual(len(resulting_calls), 2)
        self.assertEqual(resulting_calls[0][1][1], self.test_physician)
        self.assertEqual(resulting_calls[1][1][1], self.test_physician_2)

    @patch(HELPER_PATH)
    @patch(IR_SEARCH_PATH)
    def test_migrate_find_removed(self, ir_search_mock, helper_mock):
        """It should correctly search for removed model ir records"""
        ir_search_mock.return_value = self.test_model_set
        migrate(self.env.cr, None)

        ir_search_mock.assert_called_once_with([('model', 'in', self.removed)])

    @patch(HELPER_PATH, autospec=True)
    @patch(IR_SEARCH_PATH)
    def test_migrate_call_field_helper(self, ir_search_mock, helper_mock):
        """It should call update helper on all removed model field records"""
        ir_search_mock.return_value = self.test_model_set
        migrate(self.env.cr, None)

        expected_fields = self.test_model_set.mapped('field_id')
        helper_mock.assert_called_once_with(expected_fields)

    @patch(HELPER_PATH)
    @patch(IR_SEARCH_PATH)
    def test_migrate_clean_up_constraints(self, ir_search_mock, helper_mock):
        """It should clean up all constraints associated with removed models"""
        test_module_record = self.env['ir.module.module'].search([], limit=1)
        test_constraint = self.env['ir.model.constraint'].create({
            'name': 'Test Constraint',
            'model': self.test_model_record.id,
            'module': test_module_record.id,
            'type': 'u',
        })
        test_constraint_2 = self.env['ir.model.constraint'].create({
            'name': 'Test Constraint 2',
            'model': self.test_model_record_2.id,
            'module': test_module_record.id,
            'type': 'u',
        })
        test_constraint_set = test_constraint + test_constraint_2
        ir_search_mock.return_value = self.test_model_set
        migrate(self.env.cr, None)

        self.assertFalse(test_constraint_set.exists())

    @patch(HELPER_PATH)
    @patch(IR_SEARCH_PATH)
    def test_migrate_clean_up_xml_ids(self, ir_search_mock, helper_mock):
        """It should clean up XML IDs tied to removed model ir records"""
        test_xml_id_record = self.env['ir.model.data'].create({
            'name': 'Test XML ID',
            'model': 'ir.model',
            'res_id': self.test_model_record.id,
        })
        test_xml_id_record_2 = self.env['ir.model.data'].create({
            'name': 'Test XML ID 2',
            'model': 'ir.model',
            'res_id': self.test_model_record_2.id,
        })
        test_xml_id_set = test_xml_id_record + test_xml_id_record_2
        ir_search_mock.return_value = self.test_model_set
        migrate(self.env.cr, None)

        self.assertFalse(test_xml_id_set.exists())

    def test_migrate_clean_up_ir_records(self):
        """It should clean up removed model ir.model records"""
        self.env.cr.execute = Mock(wraps=self.env.cr.execute)
        migrate(self.env.cr, None)
        resulting_calls = self.env.cr.execute.mock_calls

        self.assertIn('DELETE FROM ir_model', resulting_calls[-1][1][0])
        self.assertEqual(self.removed, resulting_calls[-1][1][1])

    @patch(COPY_DATA_PATH)
    def test_practitioner_from_physician_equiv_fields(self, cp_data_mock):
        """It should accurately copy all equivalent fields"""
        cp_data_mock.return_value = [self.test_physician_data.copy()]
        _practitioner_from_physician(self.env, self.test_physician)
        resulting_practitioner = self.env['medical.practitioner'].search([
            ('code', '=', 'Test Code'),
        ])
        resulting_data = resulting_practitioner.copy_data()[0]

        del self.test_physician_data['info']
        del self.test_physician_data['specialty_id']
        del self.test_physician_data['schedule_template_ids']
        del self.test_physician_data['equiv_practitioner_id']
        self.assertDictContainsSubset(self.test_physician_data, resulting_data)

    @patch(COPY_DATA_PATH)
    def test_practitioner_from_physician_specialty(self, cp_data_mock):
        """It should accurately remap specialty_id field"""
        cp_data_mock.return_value = [self.test_physician_data]
        _practitioner_from_physician(self.env, self.test_physician)
        resulting_practitioner = self.env['medical.practitioner'].search([
            ('code', '=', 'Test Code'),
        ])
        result_specialties = resulting_practitioner.specialty_ids

        self.assertEqual(self.test_old_specialty, result_specialties)

    @patch(COPY_DATA_PATH)
    def test_practitioner_from_physician_correct_role(self, cp_data_mock):
        """It should give new practitioner correct role"""
        cp_data_mock.return_value = [self.test_physician_data]
        _practitioner_from_physician(self.env, self.test_physician)
        resulting_practitioner = self.env['medical.practitioner'].search([
            ('code', '=', 'Test Code'),
        ])

        expected_role = self.env.ref('medical_practitioner.doctor')
        self.assertEqual(resulting_practitioner.role_ids, expected_role)

    @patch(COPY_DATA_PATH)
    def test_practitioner_from_physician_same_partner(self, cp_data_mock):
        """It should give new practitioner same associated partner"""
        cp_data_mock.return_value = [self.test_physician_data]
        _practitioner_from_physician(self.env, self.test_physician)
        resulting_practitioner = self.env['medical.practitioner'].search([
            ('code', '=', 'Test Code'),
        ])

        self.assertEqual(resulting_practitioner.partner_id, self.test_partner)

    @patch(COPY_DATA_PATH)
    def test_practitioner_from_physician_reference(self, cp_data_mock):
        """It should link physician to correct new practitioner"""
        cp_data_mock.return_value = [self.test_physician_data]
        _practitioner_from_physician(self.env, self.test_physician)
        resulting_practitioner = self.env['medical.practitioner'].search([
            ('code', '=', 'Test Code'),
        ])
        resulting_reference = self.test_physician.equiv_practitioner_id

        self.assertEqual(resulting_reference, resulting_practitioner)

    @patch(COPY_DATA_PATH)
    def test_practitioner_from_physician_mail_messages(self, cp_data_mock):
        """It should move mail messages from physician to new practitioner"""
        cp_data_mock.return_value = [self.test_physician_data]
        test_message = self.env['mail.message'].create({
            'model': 'medical.physician',
        })
        physician_class = type(self.test_physician)
        with patch.object(physician_class, 'message_ids', new=test_message):
            _practitioner_from_physician(self.env, self.test_physician)
        resulting_practitioner = self.env['medical.practitioner'].search([
            ('code', '=', 'Test Code'),
        ])

        self.assertIn(test_message, resulting_practitioner.message_ids)

    @patch(COPY_DATA_PATH)
    def test_practitioner_from_physician_mail_followers(self, cp_data_mock):
        """It should move mail followers from physician to new practitioner"""
        cp_data_mock.return_value = [self.test_physician_data]
        test_follower = self.env['mail.followers'].create({
            'res_model': 'medical.physician',
            'partner_id': self.test_partner.id,
        })
        klass = type(self.test_physician)
        with patch.object(klass, 'message_follower_ids', new=test_follower):
            _practitioner_from_physician(self.env, self.test_physician)
        resulting_practitioner = self.env['medical.practitioner'].search([
            ('code', '=', 'Test Code'),
        ])
        resulting_followers = resulting_practitioner.message_follower_ids

        self.assertEqual(test_follower, resulting_followers)

    @patch('odoo.addons.base.ir.ir_attachment.IrAttachment.search')
    @patch(COPY_DATA_PATH)
    def test_practitioner_from_physician_search(self, cp_data_mock, srch_mock):
        """It should properly search for the physician's attachments"""
        cp_data_mock.return_value = [self.test_physician_data]
        _practitioner_from_physician(self.env, self.test_physician)

        expected_domains = [
            ('res_model', '=', 'medical.physician'),
            ('res_id', '=', self.test_physician.id),
        ]
        self.assertEqual(srch_mock.call_count, 1)
        self.assertEqual(srch_mock.call_args_list[0][0][0], expected_domains)

    @patch('odoo.addons.base.ir.ir_attachment.IrAttachment.search')
    @patch(COPY_DATA_PATH)
    def test_practitioner_from_physician_attach(self, cp_data_mock, srch_mock):
        """It should move attachments from physician to new practitioner"""
        cp_data_mock.return_value = [self.test_physician_data]
        test_attachment = self.env['ir.attachment'].create({
            'name': 'Test Attachment',
            'res_model': 'medical.physician',
            'res_id': self.test_physician.id,
        })
        srch_mock.return_value = test_attachment
        _practitioner_from_physician(self.env, self.test_physician)
        resulting_practitioner = self.env['medical.practitioner'].search([
            ('code', '=', 'Test Code'),
        ])
        resulting_attachments = self.env['ir.attachment'].search([
            ('res_model', '=', 'medical.practitioner'),
            ('res_id', '=', resulting_practitioner.id),
        ])

        self.assertEqual(test_attachment, resulting_attachments)
