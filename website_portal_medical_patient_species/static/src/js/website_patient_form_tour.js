/* Copyright 2017 LasLabs Inc.
 * License LGPL-3 or later (http://www.gnu.org/licenses/lgpl.html) */

 odoo.define('website_portal_medical_patient_species.patient_form_species', function (require) {
    'use strict';

    var base = require('web_editor.base');
    var _t = require('web.core')._t;
    var tour = require('web_tour.tour');

    tour.register(
        'website_portal_medical_patient_species.patient_form_species',
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
                content: _t('Change Species'),
                trigger: "label:contains('Species')",
                run: function () {
                    var species = $("select[name='species_id']");
                    species.val('1');
                    if (species === null) {
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
            }
        ]
    );
});
