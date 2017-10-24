# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).


def migrate(cr, version):
    """Connect prescription orders to correct practitioners"""
    cr.execute(
        """ALTER TABLE medical_prescription_order
        ADD practitioner_id INTEGER"""
    )
    cr.execute(
        """UPDATE medical_prescription_order
        SET practitioner_id = equiv_practitioner_id
        FROM medical_physician
        WHERE physician_id = medical_physician.id"""
    )
