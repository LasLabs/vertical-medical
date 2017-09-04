/* Copyright 2017 LasLabs Inc.
 * License LGPL-3 or later (http://www.gnu.org/licenses/lgpl.html) */

 odoo.define('website_portal_medical.my_medical_tour', function (require) {
    'use strict';

    var base = require('web_editor.base');
    var _t = require('web.core')._t;
    var tour = require('web_tour.tour');

    tour.register(
        'website_portal_medical.my_medical_tour',
        {
            test: true,
            url: '/my/medical',
            name: _t('Ensure My Medical Page loads'),
            wait_for: base.ready()
        },
        [
            {
                content: _t('Click on the My Medical navbar item'),
                trigger: "a.navbar-brand:contains('My Medical')",
                run: function () {
                    var medical_header = $("a.navbar-brand:contains('My Medical)");
                    if (medical_header === null) {
                        tour._consume_tour(
                            tour.running_tour,
                            'Did not load the my medical page properly'
                        );
                    }
                }
            }
        ]
    );
});
