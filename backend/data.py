med_records_jason = """Jason Bourne (Patient ID: P12345678) is a 53‑year‑old male (Gender Code: 1) residing in California (Branch State: CA, Branch ID: 0012345678) with ZIP code 94558. His care was initiated on 2023‑07‑15 (Start of Care Date) following a physician’s order dated 2023‑07‑14, and the written referral was received on 2023‑07‑10. The attending physician who signed the plan of care is Dr. Emily Hart (NPI: 3456789012; CMS Certification Number: AB123456). Jason’s Medicare number is HIC12345678, Medicaid number MD87654321, and his Social Security number is 123‑45‑6789. Born on 1970‑01‑20, he identifies as White (Race Code: A) and is not of Hispanic or Latino origin (Ethnicity Code: A).

At the time of assessment (completed on 2023‑07‑16 by an RN, Discipline Code: 1), Jason reported a history of hypertension and Type II diabetes managed with metformin and lisinopril. His home care is covered by private insurance (Payment Source Code: 8). Although English is his preferred language, he occasionally uses Spanish-speaking family members for interpretation (Language Code: 1; Interpreter Needed: No).

Over the past year, Jason experienced two hospital admissions for hypertensive crises, most recently in May 2023, prompting the current home health referral. He lives with his wife and two teenage children in a single‑story home; he manages daily wound care and insulin injections independently but requires assistance with balance and mobility during ambulation. No known drug allergies were documented. This comprehensive record captures Jason’s administrative details, insurance coverage, demographics, and early care history in preparation for ongoing home health services."""


chart_data = [
    {
        "title": "M0018. National Provider Identifier (NPI) for the attending physician who has signed the plan of care",
        "value": "CM126",
        "bbox": {"top": 120, "left": 80, "width": 140, "height": 20},
    },
    {
        "title": "M0010. CMS Certification Number",
        "value": "CA",
        "bbox": {"top": 150, "left": 80, "width": 50, "height": 20},
    },
    {
        "title": "M0014. Branch State",
        "value": "CA",
        "bbox": {"top": 180, "left": 80, "width": 50, "height": 20},
    },
    {
        "title": "M0016. Branch ID Number",
        "value": "999990000",
        "bbox": {"top": 210, "left": 80, "width": 100, "height": 20},
    },
    {
        "title": "M0020. Patient ID Number",
        "value": "03182025",
        "bbox": {"top": 240, "left": 80, "width": 100, "height": 20},
    },
    {
        "title": "M0030. Start of Care Date",
        "value": "03/18/2025",
        "bbox": {"top": 270, "left": 80, "width": 100, "height": 20},
    },
    {
        "title": "M0040. Patient Name",
        "value": "Jason Bourne",
        "bbox": {"top": 300, "left": 80, "width": 140, "height": 20},
    },
    {
        "title": "M0050. Patient State of Residence",
        "value": "CA",
        "bbox": {"top": 330, "left": 80, "width": 50, "height": 20},
    },
    {
        "title": "M0060. Patient ZIP Code",
        "value": "94558",
        "bbox": {"top": 360, "left": 80, "width": 60, "height": 20},
    },
    {
        "title": "M0064. Social Security Number",
        "value": "111123333",
        "bbox": {"top": 390, "left": 80, "width": 100, "height": 20},
    },
    {
        "title": "M0063. Medicare Number",
        "value": "MED777",
        "bbox": {"top": 420, "left": 80, "width": 80, "height": 20},
    },
    {
        "title": "M0065. Medicaid Number",
        "value": "x",
        "bbox": {"top": 450, "left": 80, "width": 20, "height": 20},
    },
    {
        "title": "M0069. Gender",
        "value": "1",
        "bbox": {"top": 480, "left": 80, "width": 20, "height": 20},
    },
    {
        "title": "M0066. Birth Date",
        "value": "01/09/1970",
        "bbox": {"top": 520, "left": 80, "width": 100, "height": 20},
    },
    {
        "title": "A1005. Ethnicity",
        "value": "X",
        "bbox": {"top": 560, "left": 80, "width": 20, "height": 20},
    },
    {
        "title": "A1010. Race",
        "value": ["X", "X", "X", "Z"],
        "bbox": {"top": 600, "left": 80, "width": 140, "height": 20},
    },
    {
        "title": "M0150. Current Payment Sources for Home Care",
        "value": ["0", "1"],
        "bbox": {"top": 640, "left": 80, "width": 100, "height": 20},
    },
    {
        "title": "A1110. Language",
        "value": "1",
        "bbox": {"top": 680, "left": 80, "width": 20, "height": 20},
    },
    {
        "title": "A1110.B. Interpreter needed",
        "value": "4",
        "bbox": {"top": 680, "left": 200, "width": 20, "height": 20},
    },
    {
        "title": "M0080. Discipline of Person Completing Assessment",
        "value": "1",
        "bbox": {"top": 720, "left": 80, "width": 20, "height": 20},
    },
    {
        "title": "M0090. Date Assessment Completed",
        "value": "05/14/2026",
        "bbox": {"top": 760, "left": 80, "width": 100, "height": 20},
    },
    {
        "title": "M0100. This Assessment is Currently Being Completed for the Following Reason",
        "value": "1",
        "bbox": {"top": 800, "left": 80, "width": 20, "height": 20},
    },
    {
        "title": "M0102. Date of Physician‑ordered Start of Care",
        "value": "03/18/2025",
        "bbox": {"top": 840, "left": 80, "width": 100, "height": 20},
    },
    {
        "title": "M0104. Date of Referral",
        "value": "03/15/2025",
        "bbox": {"top": 880, "left": 80, "width": 100, "height": 20},
    },
]
