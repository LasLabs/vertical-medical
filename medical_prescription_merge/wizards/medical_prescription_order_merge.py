# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import itertools
from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class MedicalPrescriptionOrderMerge(models.TransientModel):
    _name = 'medical.prescription.order.merge'

    merge_order_ids = fields.Many2many(
        comodel_name='medical.prescription.order',
        string='Orders to be Merged',
        help='List of prescription orders to be merged',
        required=True,
        default=lambda s: s._compute_default_merge_orders(),
    )
    dest_order_id = fields.Many2one(
        comodel_name='medical.prescription.order',
        string='Destination Order',
        help='This prescription order will serve as the baseline for the merge'
             ' (its info will take precedence when there are conflicts)',
        required=True,
        default=lambda s: s._compute_default_dest_order(),
        # domain='[("id", "in", merge_order_ids[0][2])]',
    )
    skip_validation = fields.Boolean(
        help='Check this box to allow prescription orders issued by different'
             ' physicians or for different dates to be merged',
        string='Skip Validation?',
    )

    def _compute_default_merge_orders(self):
        if self.env.context.get('active_model') \
                == 'medical.prescription.order':
            return self.env['medical.prescription.order'].browse(
                self.env.context.get('active_ids')
            )
        else:
            return self.env['medical.prescription.order']

    def _compute_default_dest_order(self):
        merge_order_ids = self._compute_default_merge_orders()
        if merge_order_ids:
            return merge_order_ids[0]
        else:
            return merge_order_ids

    @api.multi
    def action_merge(self):
        self.ensure_one()

        if len(self.merge_order_ids) < 2:
            raise ValidationError(_(
                'You must select at least two orders to start a merge.'
            ))

        if not self.skip_validation:
            merge_physicians = set(self.merge_order_ids.mapped('physician_id'))
            if len(merge_physicians) > 1:
                raise ValidationError(_(
                    'It can be dangerous to merge prescription orders issued'
                    ' by different physicians! If you are sure that you want'
                    ' to do this, please select the "Skip Validation?"'
                    ' checkbox and try again.'
                ))

            merge_dates = set(self.merge_order_ids.mapped('date_prescription'))
            merge_dates.discard(False)
            if len(merge_dates) > 1:
                raise ValidationError(_(
                    'It can be dangerous to merge prescription orders with'
                    ' different dates! If you are sure that you want to do'
                    ' this, please select the "Skip Validation?" checkbox and'
                    ' try again.'
                ))

        source_orders = self.merge_order_ids - self.dest_order_id
        self._perform_merge(source_orders, self.dest_order_id)

        return {'type': 'ir.actions.act_window_close'}

    def _perform_merge(self, source_orders, dest_order):
        merge_data = {}

        for field_name, field in dest_order._fields.iteritems():
            if field.compute or field.related or field.automatic \
                    or field.readonly or field.company_dependent:
                continue

            if field.type in ('many2many', 'one2many'):
                field_data = []
                for order in itertools.chain(source_orders, [dest_order]):
                    field_data += order[field_name].ids
                merge_data[field_name] = [(6, 0, field_data)]
            elif field.type == 'many2one':
                for order in itertools.chain(source_orders, [dest_order]):
                    if order[field_name]:
                        merge_data[field_name] = order[field_name].id
            else:
                for order in itertools.chain(source_orders, [dest_order]):
                    if order[field_name]:
                        merge_data[field_name] = order[field_name]

        dest_order.write(merge_data)
        source_orders.unlink()
