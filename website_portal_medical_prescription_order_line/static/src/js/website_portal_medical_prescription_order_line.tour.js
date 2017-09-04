/* Copyright 2017 LasLabs Inc.
 * License LGPL-3 or later (http://www.gnu.org/licenses/lgpl.html) */

odoo.define('website_portal_medical_prescription_order_line.patient_filter_tour', function (require) {
    'use strict';

    var base = require('web_editor.base');
    var _t = require('web.core')._t;
    var tour = require('web_tour.tour');

    tour.register(
        'website_portal_medical_prescription_order_line.patient_filter_tour',
        {
            test: true,
            url: '/my/medical',
            name: _t('Test patient filter for prescriptions on My Medical website page'),
            wait_for: base.ready()
        },
        [
            {
                content: _t('Click on Your Prescriptions'),
                trigger: "a[href='/medical/prescriptions']"
            },
            {
                content: _t('Check that filter is empty at first'),
                trigger: 'div.patient-filter-select',
                run: function () {
                    var selected = $('select.patient-filter-select').val();
                    if (selected) {
                        tour._consume_tour(
                            tour.running_tour,
                            'One or more options in the patient filter were ' +
                            'selected when it should have been empty'
                        );
                    }
                }
            },
            {
                content: _t('Check that both demo Rx lines are showing'),
                trigger: 'span[data-oe-model="medical.medicament"]',
                run: function () {
                    var demo_rx_lines = $('span:contains("Portal Rx Lines - Demo Medicament")');
                    if (demo_rx_lines.length !== 2) {
                        tour._consume_tour(
                            tour.running_tour,
                            'The filter is empty but the expected Rx lines are not showing'
                        );
                    }
                }
            },
            {
                content: _t('Select first demo patient and filter'),
                trigger: 'div.patient-filter-select',
                run: function (actions) {
                    var filter = $('select.patient-filter-select');
                    var patient_option = $('option:contains("Portal Rx Lines - Demo Patient 1")');
                    filter.val(patient_option.val()).trigger('change');
                    actions.click(filter.siblings('input'));
                }
            },
            {
                content: _t('Check that Rx lines are now filtered'),
                trigger: '.col-xs-12:only-child',
                run: function () {
                    var demo_rx_line_2 = $('span:contains("Portal Rx Lines - Demo Patient 2")');
                    if (demo_rx_line_2.length) {
                        tour._consume_tour(
                            tour.running_tour,
                            'The filter did not properly exclude the second demo Rx line'
                        );
                    }
                }
            },
            {
                content: _t('Check that filter still shows first demo patient'),
                trigger: 'div.patient-filter-select',
                run: function () {
                    var selected = $('select.patient-filter-select').val();
                    var patient_option = $('option:contains("Portal Rx Lines - Demo Patient 1")');
                    if (!selected || selected.length !== 1 || selected[0] !== patient_option.val()) {
                        tour._consume_tour(
                            tour.running_tour,
                            'The first demo patient is not selected or is ' +
                            'not the only selected option'
                        );
                    }
                }
            }
        ]
    );
});
