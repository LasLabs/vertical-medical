# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)


def pre_init_hook(cr):
    """Keep prior Rx verification data in DB by renaming relevant columns"""
    with cr.savepoint():
        verification_columns = (
            'is_verified', 'verify_date', 'verify_method', 'verify_user_id'
        )
        for column in verification_columns:
            cr.execute(
                """SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'medical_prescription_order'
                AND column_name = %s""",
                (column,)
            )
            if cr.fetchone():
                cr.execute(
                    """ALTER TABLE medical_prescription_order
                    RENAME COLUMN %s TO %s"""
                    % (column, column + '_old')
                )
