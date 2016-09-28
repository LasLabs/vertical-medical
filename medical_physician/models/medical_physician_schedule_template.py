# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models
from openerp.addons.medical.medical_constants import days, hours, minutes


class MedicalPhysicianScheduleTemplate(models.Model):
    _name = 'medical.physician.schedule.template'
    _description = 'Medical Physicians Schedule Templates'

    physician_id = fields.Many2one(
        string='Physician',
        help='Physician for the schedule template',
        comodel_name='medical.physician',
        required=True,
        select=True,
        ondelete='cascade',
    )
    day = fields.Selection(
        selection=days,
        help='Day of schedule',
        sort=False,
    )
    start_hour = fields.Selection(
        selection=hours,
        string='Hour',
        help='Starting hour available',
    )
    start_minute = fields.Selection(
        selection=minutes,
        string='Minute',
        help='Starting minute available',
    )
    end_hour = fields.Selection(
        selection=hours,
        string='Hour',
        help='Ending hour available',
    )
    end_minute = fields.Selection(
        selection=minutes,
        string='Minute',
        help='Ending minute available',
    )
    duration = fields.Selection(
        selection=minutes,
        help='Duration available',
    )
