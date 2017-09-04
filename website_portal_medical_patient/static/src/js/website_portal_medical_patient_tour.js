/* Copyright 2017 LasLabs Inc.
 * License LGPL-3 or later (http://www.gnu.org/licenses/lgpl.html) */

 odoo.define('website_portal_medical_patient.medical_patient_tour', function (require) {
    'use strict';

    var base = require('web_editor.base');
    var _t = require('web.core')._t;
    var tour = require('web_tour.tour');

    tour.register(
        'website_portal_medical_patient.medical_patient_tour',
        {
            test: true,
            url: '/my/medical',
            name: _t('Test Medical Patient Views'),
            wait_for: base.ready()
        },
        [
            {
                content: _t('Click on Your Patients'),
                trigger: "a[href='/medical/patients']"
            },
            {
                content: _t('Click on Emma Fields'),
                trigger: "a[href='/medical/patients/1']"
            },
            {
                content: _t('Change Full Name'),
                trigger: "label:contains('Full Name')",
                run: function () {
                    var input = $("input[name='name']");
                    var uom = $("select[name='weight_uom']");
                    input.val('Test');
                    uom.val('4');
                    if (input === null || uom === null) {
                        tour._consume_tour(
                            tour.running_tour,
                            'Inputs were not properly selected.'
                        );
                    }
                }
            },
            {
                content: _t('Click Save'),
                trigger: "button.o_website_form_send"
            },
            {
                content: _t('Click on Your Patients Again'),
                trigger: "a[href='/medical/patients']"
            },
            {
                content: _t('Emma Fields Should Be Test'),
                trigger: "h5:contains('Test')",
            }
        ]
    );
});
