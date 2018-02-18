/* Copyright 2017 LasLabs Inc.
 * License GPL-3 or later (http://www.gnu.org/licenses/lgpl.html) */

odoo.define('website_portal_medical_insurance_us.tour', function (require) {
    'use strict';

    var tour = require('web_tour.tour');
    var _t = require('web.core')._t;
    var base = require('web_editor.base');

    var insuranceVals = {
        patient_name: 'Gary Smith',
        number: 'ID Number',
        plan_number: 'Plan Number',
        insurance_company_name: 'New Company',
        group_number: 'Group Number',
        rx_bin: 'Rx Bin',
        rx_group: 'Rx Group',
        rx_pcn: 'Rx PCN',
    };

    tour.register(
        'website_portal_medical_insurance_us.tour',
        {
            url: '/my/medical',
            name: _t('Test insurance portal'),
            test: true,
            wait_for: base.ready(),
        },
        [
            {
                content: 'Click on Your Insurance Plans',
                trigger: "a[href='/medical/insurance/plans']",
            },
            {
                content: 'Click edit on insurance plan',
                trigger: 'div.medical-insurance-plan a',
            },
            {
                content: 'Enter company',
                trigger: 'input[name=insurance_company_name]',
                run: 'text ' + insuranceVals.insurance_company_name,
            },
            {
                content: 'Enter Group Number',
                trigger: 'input[name=group_number]',
                run: 'text ' + insuranceVals.group_number,
            },
            {
                content: 'Enter Rx Bin',
                trigger: 'input[name=rx_bin]',
                run: 'text ' + insuranceVals.rx_bin,
            },
            {
                content: 'Enter Rx PCN',
                trigger: 'input[name=rx_pcn]',
                run: 'text ' + insuranceVals.rx_pcn,
            },
            {
                content: 'Enter Rx Group',
                trigger: 'input[name=rx_group]',
                run: 'text ' + insuranceVals.rx_group,
            },
            {
                content: 'Click Save',
                trigger: 'button.o_website_form_send',
            },
            {
                content: 'Add new plan',
                trigger: 'a[href="/medical/insurance/plan"]',
            },
            {
                content: 'Enter Patient Name',
                trigger: 'input[name=patient_name]',
                run: 'text ' + insuranceVals.patient_name,
            },
            {
                content: 'Enter Company',
                trigger: 'input[name=insurance_company_name]',
                run: 'text ' + insuranceVals.insurance_company_name,
            },
            {
                content: 'Enter Identification Number',
                trigger: 'input[name=number]',
                run: 'text ' + insuranceVals.number,
            },
            {
                content: 'Enter Group Number',
                trigger: 'input[name=group_number]',
                run: 'text ' + insuranceVals.group_number,
            },
            {
                content: 'Enter Plan Number',
                trigger: 'input[name=plan_number]',
                run: 'text ' + insuranceVals.plan_number,
            },
            {
                content: 'Enter Rx Bin',
                trigger: 'input[name=rx_bin]',
                run: 'text ' + insuranceVals.rx_bin,
            },
            {
                content: 'Enter Rx PCN',
                trigger: 'input[name=rx_pcn]',
                run: 'text ' + insuranceVals.rx_pcn,
            },
            {
                content: 'Enter Rx Group',
                trigger: 'input[name=rx_group]',
                run: 'text ' + insuranceVals.rx_group,
            },
            {
                content: 'Click Save',
                trigger: 'button.o_website_form_send',
            },
            {
                content: 'Assert back at the medical screen',
                trigger: 'div.o_website_medical_insurance',
            }
        ]
    );
});
