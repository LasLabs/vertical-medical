# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class BaseKanbanStage(models.Model):
    _inherit = 'base.kanban.stage'

    @api.multi
    def write(self, vals):
        verified_stages = self.filtered('is_verified')

        super_result = super(BaseKanbanStage, self).write(vals)

        verified_stages_now = self.filtered('is_verified')
        new_verified_stages = verified_stages_now - verified_stages
        rx_line_model = self.env['medical.prescription.order.line']
        new_verified_lines = rx_line_model.search([
            ('stage_id', 'in', new_verified_stages.ids)
        ])
        new_verified_lines._sale_crm_auto()

        return super_result
