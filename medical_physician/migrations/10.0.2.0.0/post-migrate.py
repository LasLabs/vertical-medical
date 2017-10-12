# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, SUPERUSER_ID
from odoo.tools import mute_logger


# Mute logger in physician model to prevent write error messages
@mute_logger('odoo.addons.medical_physician.models.medical_physician')
def migrate(cr, version):
    """Create practitioner record for each physician and clean up"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    physician_model = env['medical.physician'].with_context(active_test=False)
    physicians = physician_model.search([])

    # Use new specialty since old record will be removed
    specialty_gp_old = env.ref('medical_physician.medical_specialty_gp')
    specialty_gp_new = env.ref('medical_practitioner.medical_specialty_gp')
    general_physicians = physicians.filtered(
        lambda r: r.specialty_id == specialty_gp_old
    )
    general_physicians.write({'specialty_id': specialty_gp_new.id})

    for physician in physicians:
        _practitioner_from_physician(env, physician)

    # Clean up ir records for models removed during migration to prevent errors
    removed_models = [
        'medical.physician.schedule.template',
        'medical.physician.service',
        'medical.physician.unavailable.wizard',
    ]
    removed_model_records = env['ir.model'].search([
        ('model', 'in', removed_models),
    ])
    removed_model_fields = removed_model_records.mapped('field_id')

    removed_model_fields._prepare_update()
    env['ir.model.constraint'].search([
        ('model', 'in', removed_model_records.ids),
    ]).unlink()
    env['ir.model.data'].search([
        ('model', '=', 'ir.model'),
        ('res_id', 'in', removed_model_records.ids),
    ]).unlink()
    cr.execute(
        'DELETE FROM ir_model WHERE model IN (%s, %s, %s)',
        removed_models,
    )


def _practitioner_from_physician(env, physician):
    vals = physician.copy_data()[0]
    vals.pop('info', None)
    vals.pop('schedule_template_ids', None)
    vals.pop('equiv_practitioner_id', None)
    vals['specialty_ids'] = [(6, 0, [vals.pop('specialty_id')])]
    vals['role_ids'] = [(6, 0, [env.ref('medical_practitioner.doctor').id])]
    vals['partner_id'] = physician.partner_id.id
    practitioner = env['medical.practitioner'].create(vals)

    write_vals = {
        'model': 'medical.practitioner',
        'res_id': practitioner.id,
    }
    physician.message_ids.write(write_vals)
    write_vals['res_model'] = write_vals.pop('model')
    practitioner.message_follower_ids.unlink()
    physician.message_follower_ids.write(write_vals)
    attachments = env['ir.attachment'].search([
        ('res_model', '=', 'medical.physician'),
        ('res_id', '=', physician.id),
    ])
    attachments.write(write_vals)

    physician.equiv_practitioner_id = practitioner
