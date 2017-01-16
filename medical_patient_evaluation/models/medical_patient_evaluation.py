# -*- coding: utf-8 -*-
# Copyright 2004-2015 Tech-Receptives
# Copyright 2015-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MedicalPatientEvaluation(models.Model):
    _name = 'medical.patient.evaluation'
    _description = 'Medical Patient Evaluation'

    patient_id = fields.Many2one(
        string='Patient',
        comodel_name='medical.patient',
        required=True,
    )
    information_source = fields.Char(
        string='Source',
        help="Source of information: Self, relative, friend, etc.",
    )
    info_diagnosis = fields.Text(
        string='Extra Info',
        help='Presumptive Diagnosis: Extra Info',
    )
    is_disoriented = fields.Boolean(
        string='Disoriented',
        help='Check this box if the patient is disoriented in time and/or'
             ' space.'
    )
    weight = fields.Float(
        string='Weight',
    )
    evaluation_type = fields.Selection(
        selection=[
            ('a', 'Ambulatory'),
            ('e', 'Emergency'),
            ('i', 'Inpatient'),
            ('pa', 'Pre-arranged appointment'),
            ('pc', 'Periodic control'),
            ('p', 'Phone call'),
            ('t', 'Telemedicine'),
        ],
        string='Type',
    )
    is_malnutritious = fields.Boolean(
        string='Malnutrition',
        help='Check this box if the patient show signs of malnutrition. If'
             ' associated to a disease, please encode the correspondent'
             ' disease on the patient disease history. For example, Moderate'
             ' protein-energy malnutrition, E44.0 in ICD-10 encoding.'
    )
    action_ids = fields.One2many(
        string='Procedures',
        comodel_name='medical.directions',
        inverse_name='evaluation_id',
        help='Procedures / Actions to take',
    )
    height = fields.Float(
        string='Height',
    )
    height_uom_id = fields.Many2one(
        string='Height Units',
        comodel_name='product.uom',
        domain="[('category_id.name', '=', 'Length')]",
    )
    is_dehydrated = fields.Boolean(
        string='Dehydration',
        help='Check this box if the patient show signs of dehydration. If'
             ' associated to a disease, please encode the correspondent'
             ' disease on the patient disease history. For example,'
             ' Volume Depletion, E86 in ICD-10 encoding.'
    )
    tag = fields.Integer(
        string='Last TAGs',
        help='Triacylglycerol(triglicerides) level. Can be approximated.'
    )
    is_tremor = fields.Boolean(
        string='Tremor',
        help='Check this box is the patient shows signs of tremors',
    )
    present_illness = fields.Text()
    evaluation_id = fields.Many2one(
        string='Appointment',
        comodel_name='medical.appointment',
        help='Enter or select the date / ID of the appointment related to'
             ' this evaluation.'
    )
    evaluation_date = fields.Datetime(
        related='evaluation_id.appointment_date',
        readonly=True,
    )
    date_start = fields.Datetime(
        string='Start',
        required=True,
    )
    date_end = fields.Datetime(
        string='End',
        required=True,
    )
    loc = fields.Integer(
        string='Level of Consciousness',
    )
    user_id = fields.Many2one(
        'res.users',
        string='Last Changed by',
        readonly=True,
    )
    mood = fields.Selection(
        selection=[
            ('n', 'Normal'),
            ('s', 'Sad'),
            ('f', 'Fear'),
            ('r', 'Rage'),
            ('h', 'Happy'),
            ('d', 'Disgust'),
            ('e', 'Euphoria'),
            ('fl', 'Flat'),
        ],
    )
    physician_id = fields.Many2one(
        string='Doctor',
        comodel_name='medical.physician',
        readonly=True,
    )
    specialty_id = fields.Many2one(
        string='Specialty',
        comodel_name='medical.specialty',
        related='physician_id.specialty_id',
    )
    is_incognizant = fields.Boolean(
        string='Knowledge of Current Events',
        help='Check this box if the patient can not respond to public'
             ' notorious events.',
    )
    next_evaluation_id = fields.Many2one(
        string='Next Appointment',
        comodel_name='medical.appointment',
    )
    signs_and_symptoms_ids = fields.One2many(
        string='Signs and Symptoms',
        comodel_name='medical.signs_and_symptoms',
        inverse_name='evaluation_id',
        help="Enter the Signs and Symptoms for the patient in this"
             " evaluation.",
    )
    loc_motor = fields.Selection(
        selection=[
            ('1', 'Makes no movement'),
            ('2', 'Extension to painful stimuli - decerebrate response -'),
            ('3',
             'Abnormal flexion to painful stimuli (decorticate response)'),
            ('4', 'Flexion / Withdrawal to painful stimuli'),
            ('5', 'Localizes painful stimuli'),
            ('6', 'Obeys commands'),
        ],
        string='Glasgow - Motor',
    )
    is_reliable_info = fields.Boolean(
        string='Reliable',
        default=True,
        help="Uncheck this option if the information provided by the source "
             "seems like it may not be not reliable.",
    )
    systolic = fields.Integer(
        string='Systolic Pressure',
    )
    vocabulary = fields.Boolean(
        string='Vocabulary',
        help='Check this box if the patient lacks basic intellectual'
             ' capacity, when she/he can not describe elementary objects.',
    )
    is_catatonic = fields.Boolean(
        string='Catatonic',
        help='Check this box if the patient is unable to make voluntary'
             'movements.',
    )
    hip = fields.Float(
        string='Hip',
        help='Hip circumference.',
    )
    hip_uom_id = fields.Many2one(
        string='Hip Units',
        comodel_name='product.uom',
        domain="[('category_id.name', '=', 'Length')]",
    )
    is_forgetful = fields.Boolean(
        string='Memory',
        help='Check this box if the patient has problems in short or long'
             ' term memory.',
    )
    is_abnormal_reasoning = fields.Boolean(
        string='Abnormal Reasoning',
        help='Check this box if the patient presents abnormalities in'
             ' abstract reasoning.'
    )
    referred_from_id = fields.Many2one(
        string='Derived/Referred From',
        comodel_name='medical.physician',
        help='Physician who derived/referred the case',
    )
    loc_verbal = fields.Selection(
        selection=[
            ('1', 'Makes no sounds'),
            ('2', 'Incomprehensible sounds'),
            ('3', 'Utters inappropriate words'),
            ('4', 'Confused, disoriented'),
            ('5', 'Oriented, converses normally'),
        ],
        string='Glasgow - Verbal',
    )
    glycemia = fields.Float(
        string='Glycemia',
        help='Last blood glucose level. Can be approximated.',
    )
    head_circumference = fields.Float(
        string='Head Circumference',
        help='Head Circumference',
    )
    head_circumference_uom_id = fields.Many2one(
        string='Head Circumference Units',
        comodel_name='product.uom',
        domain="[('category_id.name', '=', 'Length')]",
    )
    bmi = fields.Float(
        string='BMI',
        help='Body mass index.',
    )
    respiratory_rate = fields.Integer(
        string='Respiratory Rate',
        help='Respiratory rate expressed in breaths per minute.',
    )
    referred_to_id = fields.Many2one(
        string='Referred To',
        comodel_name='medical.physician',
        help='Physician to escalate / refer the case to.',
    )
    hba1c = fields.Float(
        string='Glycated Hemoglobin',
        help='Last Glycated Hb level. Can be approximated.',
    )
    is_violent = fields.Boolean(
        string='Violent Behavior',
        help='Check this box if the patient is aggressive or violent at the'
             ' moment.'
    )
    directions = fields.Text(
        string='Plan',
    )
    evaluation_summary = fields.Text()
    cholesterol_total = fields.Integer(
        string='Last Cholesterol',
    )
    hypothesis_ids = fields.One2many(
        string='Hypotheses / DDx',
        comodel_name='medical.patient.evaluation.hypothesis',
        inverse_name='evaluation_id',
        help='Presumptive Diagnosis. If no diagnosis can be made, '
             'encode the main sign or symptom.',
    )
    no_judgment = fields.Boolean(
        string='Judgment',
        help='Check this box if the patient can not interpret basic'
             ' scenario solutions.',
    )
    temperature = fields.Float(
        string='Temperature',
        help='Temperature in Celcius.',
    )
    osat = fields.Integer(
        string='Oxygen Saturation',
        help='Oxygen Saturation(arterial).',
    )
    secondary_condition_ids = fields.One2many(
        string='Secondary Conditions',
        comodel_name='medical.condition',
        inverse_name='evaluation_id',
        help="Other, Secondary conditions found on the patient",
    )
    calculation_ability = fields.Boolean(
        string='Calculation Ability',
        help='Check this box if the patient can not do simple arithmetic'
             ' problems.',
    )
    bpm = fields.Integer(
        string='Heart Rate',
        help='Heart rate expressed in beats per minute',
    )
    chief_complaint_id = fields.Many2one(
        string='Chief Complaint',
        comodel_name='medical.condition',
        required=True,
        help='Chief Complaint',
    )
    loc_eyes = fields.Selection(
        selection=[
            ('1', 'Does not Open Eyes'),
            ('2', 'Opens eyes in response to painful stimuli'),
            ('3', 'Opens eyes in response to voice'),
            ('4', 'Opens eyes spontaneously'),
        ],
        string='Glasgow - Eyes',
    )
    abdominal_circumference = fields.Float(
        string='Waist',
        help='Abdominal circumference.',
    )
    abdominal_circumference_uom_id = fields.Many2one(
        string='Wait Units',
        comodel_name='product.uom',
        domain="[('category_id.name', '=', 'Length')]",
    )
    no_recognition = fields.Boolean(
        string='Object Recognition',
        help='Check this box if the patient suffers from any sort of'
             ' gnosia disorders - such as agnosia, prosopagnosia, etc.',
    )
    diagnosis_id = fields.Many2one(
        string='Presumptive Diagnosis',
        comodel_name='medical.pathology',
    )
    whr = fields.Float(
        string='WHR',
        help='Waist to hip ratio',
    )
    ldl = fields.Integer(
        string='Last LDL',
        help='Last LDL Cholesterol reading. Can be approximated.',
    )
    hdl = fields.Integer(
        string='Last HDL',
    )
    diastolic = fields.Integer(
        string='Diastolic Pressure',
    )
    notes = fields.Text()
