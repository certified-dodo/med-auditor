"""
In-memory sample medical records and charts with intentional discrepancies
for testing the discrepancy checking functionality.
"""

# Dictionary of medical records, keyed by MRN
medical_records = {
    "91283": """MEDICAL RECORD - MRN: 91283
PATIENT NAME: John Smith
DATE OF BIRTH: 05/22/1962
PRIMARY DIAGNOSIS: Type 2 Diabetes Mellitus (E11.9), Hypertension (I10)
VITAL SIGNS: BP 140/85, HR 72, RR 16, Temp 98.6F, O2 sat 98%
ASSESSMENT:
- Blood glucose levels have been fluctuating between 130-200 mg/dL
- Patient reports occasional dizziness upon standing
- Feet examination shows no ulcers or signs of neuropathy
- Blood pressure slightly elevated despite medication compliance
MEDICATIONS:
- Metformin 1000mg BID
- Lantus 30 units qHS
- Novolog sliding scale as directed
- Lisinopril 20mg daily
PLAN:
- Continue current medication regimen
- Blood glucose monitoring 4x daily
- Follow up appointment in 2 weeks
- Dietary consultation for carbohydrate counting education
- Referral to diabetes education program""",

    "65441": """MEDICAL RECORD - MRN: 65441
PATIENT NAME: Sarah Johnson
DATE OF BIRTH: 11/14/1975
PRIMARY DIAGNOSIS: Congestive Heart Failure (I50.9), Atrial Fibrillation (I48.91)
VITAL SIGNS: BP 130/80, HR 88 irregular, RR 20, Temp 98.8F, O2 sat 95% on RA
ASSESSMENT:
- Patient reports decreased exercise tolerance, can walk only 1 block before SOB
- Bilateral lower extremity edema +2
- Lungs with bibasilar crackles
- Daily weight shows 2lb gain over past week
- Sleep requiring 3 pillows (increased from baseline)
MEDICATIONS:
- Lasix 40mg BID
- Metoprolol 25mg BID
- Eliquis 5mg BID
- Potassium Chloride 20mEq daily
- Lisinopril 10mg daily
PLAN:
- Increase Lasix to 60mg BID for 3 days, then return to 40mg BID
- Daily weights
- Fluid restriction to 1.5L daily
- Low sodium diet reinforcement
- Call if weight increases by >3lbs in 24 hours or >5lbs in a week""",

    "78392": """MEDICAL RECORD - MRN: 78392
PATIENT NAME: Maria Garcia
DATE OF BIRTH: 03/08/1985
PRIMARY DIAGNOSIS: Asthma (J45.909), Allergic Rhinitis (J30.9)
VITAL SIGNS: BP 118/70, HR 75, RR 18, Temp 98.4F, O2 sat 99% on RA
ASSESSMENT:
- Patient reports increased use of rescue inhaler, 3-4 times per week
- Occasional nighttime awakening due to cough/wheeze
- Peak flow measurements 80-85% of personal best
- Nasal congestion worse during spring months
MEDICATIONS:
- Flovent HFA 110mcg 2 puffs BID
- ProAir HFA 90mcg 2 puffs q4h PRN shortness of breath
- Flonase 50mcg 2 sprays each nostril daily
- Zyrtec 10mg daily
PLAN:
- Continue current medication regimen
- Add Singulair 10mg daily
- Avoid known triggers (pollen, dust, pet dander)
- Review proper inhaler technique
- Follow up in 1 month to assess symptom control"""
}

# Dictionary of chart submissions, keyed by MRN
charts = {
    "91283": """CHART SUBMISSION
PATIENT: MRN-91283
DATE OF SERVICE: 03/15/2024
SERVICE TYPE: Skilled Nursing - Diabetic care
VITAL SIGNS: BP 165/95, HR 88, RR 18, Temp 98.8F, O2 sat 96%
MEDICATIONS ADMINISTERED/REVIEWED: Lantus 30 units qHS, Novolog sliding scale, Metformin 1000mg daily, Lisinopril 20mg daily
ASSESSMENT: Patient reports blood glucose readings 140-220mg/dL over past week. Continuing to experience occasional dizziness. Feet examined - no ulcers or lesions noted.
INTERVENTIONS: Reinforced proper medication administration and timing. Reviewed blood glucose log. Provided education on dietary choices to manage blood glucose levels.
PLAN: Continue monitoring blood glucose 4x daily. Follow up appointment scheduled for 03/29/2024.""",

    "65441": """CHART SUBMISSION
PATIENT: MRN-65441
DATE OF SERVICE: 03/16/2024
SERVICE TYPE: Skilled Nursing - CHF Management
VITAL SIGNS: BP 142/86, HR 90 (irregular), RR 22, Temp 98.6F, O2 sat 93% on RA
MEDICATIONS ADMINISTERED/REVIEWED: Lasix 40mg daily, Metoprolol 25mg BID, Eliquis 5mg BID, Potassium Chloride 20mEq daily, Lisinopril 10mg daily
ASSESSMENT: Patient reports increased shortness of breath when walking short distances. Lower extremity edema +3 bilaterally. Crackles in lung bases. Weight increased by 4lbs since last visit 3 days ago.
INTERVENTIONS: Reinforced importance of fluid restriction and low sodium diet. Reviewed daily weight log. Instructed on symptoms requiring immediate medical attention.
PLAN: Contact physician to report weight gain and increased symptoms. Continue daily weights.""",

    "78392": """CHART SUBMISSION
PATIENT: MRN-78392
DATE OF SERVICE: 03/14/2024
SERVICE TYPE: Skilled Nursing - Respiratory Care
VITAL SIGNS: BP 120/74, HR 78, RR 20, Temp 98.6F, O2 sat 97% on RA
MEDICATIONS ADMINISTERED/REVIEWED: Flovent HFA 110mcg 2 puffs daily, ProAir HFA 90mcg 2 puffs q4h PRN, Flonase 50mcg 2 sprays each nostril daily, Zyrtec 10mg daily
ASSESSMENT: Patient reports using rescue inhaler 2-3 times this week. No nighttime awakenings. Peak flow 400 (90% of personal best). Nasal congestion improved.
INTERVENTIONS: Observed inhaler technique - proper. Reviewed asthma action plan. Discussed importance of taking controller medications even when feeling well.
PLAN: Follow up appointment with pulmonologist scheduled for 04/15/2024. Continue current medication regimen."""
} 