# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).


def migrate(cr, version):
    """Update new practitioner fields based on associated physician data"""
    cr.execute(
        """UPDATE medical_practitioner
        SET is_verified = medical_physician.is_verified,
        verified_by_id = medical_physician.verified_by_id,
        verified_date = medical_physician.verified_date
        FROM medical_physician
        WHERE medical_practitioner.id = equiv_practitioner_id"""
    )
