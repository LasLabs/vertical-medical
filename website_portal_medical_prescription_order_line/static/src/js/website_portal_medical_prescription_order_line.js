/* Copyright 2017 LasLabs Inc.
 * License LGPL-3 or later (http://www.gnu.org/licenses/lgpl.html) */

odoo.define('website_portal_medical_prescription_order_line.patient_filter', function(require) {
    'use strict';

    var base = require('web_editor.base');
    base.ready().done(function() {
        $('.patient-filter-select').select2({
            placeholder: 'Select patient(s)',
            allowClear: true
        });
    });
});
