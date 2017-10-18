# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).


def migrate(cr, version):
    """Connect diseases to correct practitioners"""
    cr.execute(
        """UPDATE medical_patient_disease
        SET practitioner_id = equiv_practitioner_id
        FROM medical_physician
        WHERE physician_id = medical_physician.id"""
    )
