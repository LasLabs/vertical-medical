# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.addons.medical_prescription_state_verify.hooks import pre_init_hook


def migrate(cr, version):
    """Preserve Rx verification data via hook that renames relevant columns"""
    pre_init_hook(cr)
