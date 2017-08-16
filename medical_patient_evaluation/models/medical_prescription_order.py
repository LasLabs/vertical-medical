# -*- coding: utf-8 -*-
# Copyright 2004-2015 Tech-Receptives
# Copyright 2015-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class MedicalPrescriptionOrder(models.Model):
    _inherit = 'medical.prescription.order'

    def print_prescription(self, cr, uid, ids, context=None):
        """
        """
        #        assert len(ids) == 1, 'This option should only be used for '
        #                              'a single id at a time'
        #        wf_service = netsvc.LocalService("workflow")
        #        wf_service.trg_validate(uid, 'medical.prescription.order',
        #                                ids[0], 'prescription_sent', cr)
        datas = {
            'model': 'medical.prescription.order',
            'ids': ids,
            'drug_form_id': self.read(cr, uid, ids[0], context=context),
        }
        return {'type': 'ir.actions.report.xml',
                'report_name': 'prescription.order',
                'datas': datas,
                'nodestroy': True}


class MedicalPrescriptionOrderLine(models.Model):
    _inherit = 'medical.prescription.order.line'

    is_printed = fields.Boolean(
        help='Check this box to print this line of the prescription.',
        default=True)
    refills = fields.Integer(string='Refills #')
    review = fields.Datetime()
