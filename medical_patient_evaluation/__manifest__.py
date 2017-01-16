# -*- coding: utf-8 -*-
# Copyright 2004-2009 Tiny SPRL
# Copyright 2015-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{

    "name": "Medical EMR : Electronic Medical Record management for Medical",
    "version": "9.0.1.1",
    "author": "LasLabs, Odoo Community Association (OCA)",
    "category": "Medical",
    "depends": ["medical"],
    "website": "http://github.com/oca/vertical-medical",
    "license": "AGPL-3",
    "depends": [
        "medical_patient_disease",
        "medical_appointment",
    ],
    "data": [
        "views/medical_sequence.xml",
        "views/medical_secondary_condition_view.xml",
        "views/medical_signs_and_symptoms_view.xml",
        "views/medical_directions_view.xml",
        "views/medical_ethnicity_view.xml",
        "views/medical_prescription_order_view.xml",
        "views/medical_medicament_category_view.xml",
        "views/medical_diagnostic_hypothesis_view.xml",
        "views/medical_procedure_view.xml",
        "views/medical_medication_template_view.xml",
        "views/medical_medication_dosage_view.xml",
        "views/medical_family_member_view.xml",
        "views/medical_drug_form_view.xml",
        "views/medical_patient_medication_view.xml",
        "views/medical_patient_evaluation_view.xml",
        "views/medical_prescription_line_view.xml",
        "views/medical_patient_view.xml",
        "views/medical_drug_route_view.xml",
        "views/medical_family_view.xml",
        "views/medical_occupation_view.xml",
        "views/medical_medicament_view.xml",
        "security/ir.model.access.csv",
        "medical_menu.xml",
    ],
    "installable": False,
    "application": False,
}
