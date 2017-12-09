# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class MedicalPrescriptionOrder(models.Model):
    """ Add Kanban functionality to MedicalPrescriptionOrder """
    _inherit = ['medical.prescription.order', 'base.kanban.abstract']
    _name = 'medical.prescription.order'

    stage_id = fields.Many2one(
        required=True,
    )
