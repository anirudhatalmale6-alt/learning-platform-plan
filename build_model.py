#!/usr/bin/env python3
"""Build SmartStudent-Pune-Market-Model.xlsx — a live, editable sizing model.

Every derived figure is a real Excel formula pointing at the Assumptions sheet,
so the client can change an input and watch the whole model move.
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

# ---------------------------------------------------------------- styling
NAVY = "1F3A5F"
YELLOW = "FFF3C4"
GREY = "F2F4F7"
GREEN = "E3F2E1"

H1 = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
H2 = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
BOLD = Font(name="Calibri", size=11, bold=True)
BODY = Font(name="Calibri", size=11)
SMALL = Font(name="Calibri", size=9, italic=True, color="666666")

FILL_NAVY = PatternFill("solid", fgColor=NAVY)
FILL_INPUT = PatternFill("solid", fgColor=YELLOW)
FILL_GREY = PatternFill("solid", fgColor=GREY)
FILL_GREEN = PatternFill("solid", fgColor=GREEN)

thin = Side(style="thin", color="D0D5DD")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)

WRAP = Alignment(wrap_text=True, vertical="top")


def title(ws, text, span):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=span)
    c = ws.cell(row=1, column=1, value=text)
    c.font = H1
    c.fill = FILL_NAVY
    c.alignment = Alignment(vertical="center", indent=1)
    ws.row_dimensions[1].height = 30


def header(ws, row, labels, widths=None):
    for i, lab in enumerate(labels, start=1):
        c = ws.cell(row=row, column=i, value=lab)
        c.font = H2
        c.fill = FILL_NAVY
        c.border = BOX
        c.alignment = WRAP
    if widths:
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 28


# ================================================================ 1. README
ws = wb.active
ws.title = "How to use"
title(ws, "SmartStudent — Pune Market Model", 3)
ws.column_dimensions["A"].width = 3
ws.column_dimensions["B"].width = 100

lines = [
    ("", ""),
    ("WHAT THIS IS", "h"),
    ("A live sizing model for the SmartStudent platform, scoped to Pune city only. "
     "Every figure on the Funnel, Revenue and Unit Economics sheets is a formula "
     "driven by the Assumptions sheet.", "p"),
    ("", ""),
    ("HOW TO USE IT", "h"),
    ("1. Open the 'Assumptions' sheet. Every YELLOW cell is an input you can change.", "p"),
    ("2. Change one, and every number on the other sheets updates immediately.", "p"),
    ("3. Nothing else should be edited — grey and green cells are calculated.", "p"),
    ("", ""),
    ("IMPORTANT — READ BEFORE USING THESE NUMBERS ANYWHERE", "h"),
    ("These are MODELLED ESTIMATES, not researched facts. I have shown the full "
     "derivation so you can see exactly which assumption drives which output, and "
     "the 'Sources' sheet names the specific place to get each real number.", "p"),
    ("Do not put these figures into an investor deck or a bank proposal until the "
     "inputs flagged with a confidence of LOW have been replaced with real data.", "p"),
    ("", ""),
    ("THE ONE THING WORTH DOING FIRST", "h"),
    ("UDISE+ (udiseplus.gov.in) publishes school-level enrolment for Pune district, "
     "filterable by board and grade, for free. About a day of work there replaces "
     "the entire top half of this model with hard data. Do that before spending "
     "any money on the build.", "p"),
    ("", ""),
    ("SHEETS", "h"),
    ("Assumptions      — every input, with a confidence rating and a source to check", "p"),
    ("Market Funnel    — TAM to SAM to SOM, derived", "p"),
    ("Revenue Model    — month 12 and month 24 projection, Pune only", "p"),
    ("Unit Economics   — B2B2C vs B2C direct, side by side", "p"),
    ("Pune Ceiling     — what Pune alone maxes out at, and why that matters", "p"),
    ("Sources          — where to get each real number", "p"),
]
r = 3
for text, kind in lines:
    c = ws.cell(row=r, column=2, value=text)
    if kind == "h":
        c.font = Font(size=11, bold=True, color=NAVY)
    else:
        c.font = BODY
        c.alignment = WRAP
    r += 1

# ============================================================ 2. ASSUMPTIONS
ws = wb.create_sheet("Assumptions")
title(ws, "Assumptions — edit the yellow cells only", 5)
header(ws, 3, ["#", "Assumption", "Value", "Confidence", "Basis / what to check"],
       [5, 46, 14, 13, 62])

# (label, value, number_format, confidence, basis)
A = [
    ("POPULATION & COHORT", None, None, None, None),
    ("Pune urban agglomeration population, 2026", 7400000, "#,##0", "LOW",
     "Census 2011 UA ~5.05M extrapolated at ~2.7%/yr. Verify vs PMRDA projections."),
    ("Share of population aged 12-17", 0.095, "0.0%", "LOW",
     "Urban metros run below the national ~11% (lower fertility). Verify vs Census age tables."),
    ("School enrolment rate, urban, this age band", 0.96, "0.0%", "MEDIUM",
     "Urban Maharashtra secondary enrolment. Verify vs UDISE+."),
    ("", None, None, None, None),
    ("BOARD SPLIT (must sum to 100%)", None, None, None, None),
    ("Maharashtra SSC / HSC", 0.60, "0.0%", "LOW", "UDISE+ gives the exact Pune district split. REPLACE THIS."),
    ("CBSE", 0.24, "0.0%", "LOW", "CBSE affiliated-school directory, filter by district."),
    ("ICSE / ISC", 0.09, "0.0%", "LOW", "CISCE school locator."),
    ("IGCSE / IB", 0.02, "0.0%", "LOW", "Small; count schools directly, there are few."),
    ("Other", 0.05, "0.0%", "LOW", ""),
    ("", None, None, None, None),
    ("ADDRESSABILITY FILTERS", None, None, None, None),
    ("Has smartphone + home data access", 0.88, "0.0%", "MEDIUM", "Urban Pune penetration is high. TRAI / IAMAI reports."),
    ("Household already pays for supplementary learning", 0.55, "0.0%", "LOW",
     "NSSO Household Social Consumption: Education survey."),
    ("Of those, will pay for a DIGITAL product", 0.35, "0.0%", "LOW",
     "THE MOST IMPORTANT AND LEAST CERTAIN INPUT. Test with a landing page + Rs 15k of ads."),
    ("", None, None, None, None),
    ("THE WEDGE (SSC, Grades 9-10)", None, None, None, None),
    ("Share of SSC students in Grades 9-10", 0.36, "0.0%", "MEDIUM",
     "2 of 6 grades = 33%, weighted up slightly for board-year focus."),
    ("Reachable via coaching classes / schools", 0.60, "0.0%", "LOW",
     "Count Pune coaching institutes via GST directory + Google Maps."),
    ("Share of that reachable pool won by month 24", 0.05, "0.0%", "LOW", "Judgement. 4-7% is the plausible band."),
    ("", None, None, None, None),
    ("PRICING", None, None, None, None),
    ("Institute seat price, per student per month (Rs)", 90, "#,##0", "MEDIUM", "Validate with 15 coaching class visits."),
    ("Institute platform fee, per month (Rs)", 6000, "#,##0", "MEDIUM", "Test engine + batches + analytics + branding."),
    ("B2C direct price, per year (Rs)", 1999, "#,##0", "MEDIUM", "Anchored below Physics Wallah's reference price."),
    ("", None, None, None, None),
    ("TRACTION — MONTH 12", None, None, None, None),
    ("Institutes signed", 12, "#,##0", "LOW", "Judgement, assumes founder-led sales."),
    ("Avg paying students per institute", 110, "#,##0", "MEDIUM", "Typical mid-size Pune tutorial batch load."),
    ("B2C direct paying students", 400, "#,##0", "LOW", "Organic + referral only; no paid ads in year 1."),
    ("", None, None, None, None),
    ("TRACTION — MONTH 24", None, None, None, None),
    ("Institutes signed", 40, "#,##0", "LOW", "Judgement."),
    ("Avg paying students per institute", 130, "#,##0", "MEDIUM", ""),
    ("B2C direct paying students", 1800, "#,##0", "LOW", ""),
    ("", None, None, None, None),
    ("COST SIDE", None, None, None, None),
    ("AI + infra cost per student per month (Rs)", 28, "#,##0", "MEDIUM",
     "Assumes the AI Gateway response cache is built. Without it, budget Rs 60-120."),
    ("CAC per student — institute channel (Rs)", 180, "#,##0", "LOW", "One sale brings 100+ students."),
    ("CAC per student — B2C direct (Rs)", 1000, "#,##0", "LOW", "Parent-facing acquisition is expensive."),
    ("Annual retention — institute channel", 0.70, "0.0%", "LOW", "Institutes renew in bulk."),
    ("Annual retention — B2C direct", 0.35, "0.0%", "LOW", "Weak point of the B2C model."),
]

ref = {}
r = 4
n = 0
for label, val, fmt, conf, basis in A:
    if label == "":
        r += 1
        continue
    if val is None:  # section header
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
        c = ws.cell(row=r, column=1, value=label)
        c.font = Font(size=10, bold=True, color=NAVY)
        c.fill = FILL_GREY
        c.border = BOX
        r += 1
        continue
    n += 1
    ws.cell(row=r, column=1, value=n).font = BODY
    ws.cell(row=r, column=2, value=label).font = BODY
    vc = ws.cell(row=r, column=3, value=val)
    vc.fill = FILL_INPUT
    vc.font = BOLD
    vc.number_format = fmt
    cc = ws.cell(row=r, column=4, value=conf)
    cc.font = Font(size=10, bold=True,
                   color="B42318" if conf == "LOW" else "B54708" if conf == "MEDIUM" else "027A48")
    cc.alignment = Alignment(horizontal="center")
    bc = ws.cell(row=r, column=5, value=basis)
    bc.font = SMALL
    bc.alignment = WRAP
    for col in range(1, 6):
        ws.cell(row=r, column=col).border = BOX
    ref[label] = f"Assumptions!$C${r}"
    r += 1

# board split checksum
ws.cell(row=r + 1, column=2, value="Board split check (must equal 100%)").font = BOLD
chk = ws.cell(row=r + 1, column=3,
              value=f"={ref['Maharashtra SSC / HSC']}+{ref['CBSE']}+{ref['ICSE / ISC']}"
                    f"+{ref['IGCSE / IB']}+{ref['Other']}")
chk.number_format = "0.0%"
chk.font = BOLD
chk.fill = FILL_GREEN
chk.border = BOX

ws.freeze_panes = "A4"

P = ref  # shorthand

# ========================================================== 3. MARKET FUNNEL
ws = wb.create_sheet("Market Funnel")
title(ws, "Market funnel — Pune city, Grades 7-12", 4)
header(ws, 3, ["Step", "Value", "Formula in words", "Note"], [46, 18, 44, 40])

# (key, label, formula-template, fmt, how, note)
# A template may reference an earlier row by its key in braces — resolved against
# the actual assigned row in a second pass, so inserting or moving a spacer row
# can never silently break a reference. Labels never start with "=", or Excel
# parses the label itself as a formula.
rows = [
    ("pop", "Pune urban agglomeration population, 2026",
     f"={P['Pune urban agglomeration population, 2026']}", "#,##0", "input", ""),
    ("age", "  x share aged 12-17", f"={P['Share of population aged 12-17']}", "0.0%", "input", ""),
    ("band", "→ children in the Grade 7-12 age band", "={pop}*{age}", "#,##0", "population x age share", ""),
    ("enr", "  x school enrolment rate", f"={P['School enrolment rate, urban, this age band']}",
     "0.0%", "input", ""),
    ("tam", "→ TAM: students in school, Grades 7-12", "={band}*{enr}", "#,##0", "age band x enrolment",
     "Total addressable market, Pune"),
    (None, "", "", "", "", ""),
    ("ssc", "SSC / HSC students", "={tam}*" + P['Maharashtra SSC / HSC'], "#,##0",
     "TAM x SSC share", "The beachhead"),
    ("cbse", "CBSE students", "={tam}*" + P['CBSE'], "#,##0", "TAM x CBSE share", "Phase 3 expansion"),
    ("icse", "ICSE / ISC students", "={tam}*" + P['ICSE / ISC'], "#,##0", "TAM x ICSE share", "Later"),
    ("igcse", "IGCSE / IB students", "={tam}*" + P['IGCSE / IB'], "#,##0", "TAM x IGCSE share",
     "Last — licensing risk"),
    (None, "", "", "", "", ""),
    ("phone", "  x has smartphone + data", f"={P['Has smartphone + home data access']}", "0.0%", "input", ""),
    ("reach", "→ digitally reachable students", "={tam}*{phone}", "#,##0", "TAM x reachability", ""),
    ("pays", "  x household pays for supplementary learning",
     f"={P['Household already pays for supplementary learning']}", "0.0%", "input", ""),
    ("payhh", "→ students in paying households", "={reach}*{pays}", "#,##0",
     "reachable x paying households", ""),
    ("dig", "  x will pay for a DIGITAL product", f"={P['Of those, will pay for a DIGITAL product']}",
     "0.0%", "input", "Least certain input in the model"),
    ("sam", "→ SAM: serviceable addressable market", "={payhh}*{dig}", "#,##0",
     "paying households x digital willingness", "Pune, all boards, Grades 7-12"),
    (None, "", "", "", "", ""),
    ("wedge", "SSC students in Grades 9-10", "={ssc}*" + P['Share of SSC students in Grades 9-10'], "#,##0",
     "SSC students x grade 9-10 share", "The wedge cohort"),
    ("inst", "  x reachable via institutes", f"={P['Reachable via coaching classes / schools']}",
     "0.0%", "input", ""),
    ("pool", "→ institute-reachable wedge pool", "={wedge}*{inst}", "#,##0", "wedge x institute reach", ""),
    ("cap", "  x share won by month 24", f"={P['Share of that reachable pool won by month 24']}",
     "0.0%", "input", ""),
    ("som", "→ SOM: winnable paying students, month 24", "={pool}*{cap}", "#,##0", "pool x capture rate",
     "Cross-check against the Revenue Model sheet"),
]

# pass 1 — assign a row to every key
at = {}
r = 4
for key, label, *_ in rows:
    if key:
        at[key] = r
    r += 1

# pass 2 — write, resolving {key} placeholders to real cell addresses
r = 4
for key, label, formula, fmt, how, note in rows:
    if not key:
        r += 1
        continue
    resolved = formula.format(**{k: f"$B${v}" for k, v in at.items()})
    lc = ws.cell(row=r, column=1, value=label)
    vc = ws.cell(row=r, column=2, value=resolved)
    vc.number_format = fmt
    hc = ws.cell(row=r, column=3, value=how)
    nc = ws.cell(row=r, column=4, value=note)
    hc.font = SMALL
    nc.font = SMALL
    nc.alignment = WRAP
    if label.startswith("→"):
        lc.font = BOLD
        vc.font = BOLD
        vc.fill = FILL_GREEN
    else:
        lc.font = BODY
        vc.font = BODY
        vc.fill = FILL_GREY
    for col in range(1, 5):
        ws.cell(row=r, column=col).border = BOX
    r += 1

SAM_CELL = f"'Market Funnel'!$B${at['sam']}"
ws.freeze_panes = "A4"

# ========================================================== 4. REVENUE MODEL
ws = wb.create_sheet("Revenue Model")
title(ws, "Revenue projection — Pune only", 4)
header(ws, 3, ["Line", "Month 12", "Month 24", "Note"], [46, 18, 18, 48])

# The month-12 and month-24 traction rows share labels, so `ref` only kept the
# last occurrence of each. Resolve those three by scanning the sheet instead.
ws_a = wb["Assumptions"]
inst_rows, avg_rows, b2c_rows = [], [], []
for row in range(4, 80):
    v = ws_a.cell(row=row, column=2).value
    if v == "Institutes signed":
        inst_rows.append(row)
    elif v == "Avg paying students per institute":
        avg_rows.append(row)
    elif v == "B2C direct paying students":
        b2c_rows.append(row)

I12, I24 = f"Assumptions!$C${inst_rows[0]}", f"Assumptions!$C${inst_rows[1]}"
A12, A24 = f"Assumptions!$C${avg_rows[0]}", f"Assumptions!$C${avg_rows[1]}"
C12, C24 = f"Assumptions!$C${b2c_rows[0]}", f"Assumptions!$C${b2c_rows[1]}"
SEAT = P["Institute seat price, per student per month (Rs)"]
PLAT = P["Institute platform fee, per month (Rs)"]
B2CP = P["B2C direct price, per year (Rs)"]
AICOST = P["AI + infra cost per student per month (Rs)"]

lines = [
    ("Institutes signed", f"={I12}", f"={I24}", "#,##0", ""),
    ("Avg paying students per institute", f"={A12}", f"={A24}", "#,##0", ""),
    ("Students via institutes", "=B4*B5", "=C4*C5", "#,##0", ""),
    ("B2C direct paying students", f"={C12}", f"={C24}", "#,##0", "Organic + referral only"),
    ("TOTAL PAYING STUDENTS", "=B6+B7", "=C6+C7", "#,##0", ""),
    ("", "", "", "", ""),
    ("Institute seat revenue (Rs/yr)", f"=B6*{SEAT}*12", f"=C6*{SEAT}*12", "#,##0", "seats x price x 12"),
    ("Institute platform fees (Rs/yr)", f"=B4*{PLAT}*12", f"=C4*{PLAT}*12", "#,##0", "institutes x fee x 12"),
    ("B2C direct revenue (Rs/yr)", f"=B7*{B2CP}", f"=C7*{B2CP}", "#,##0", ""),
    ("TOTAL ARR (Rs)", "=B10+B11+B12", "=C10+C11+C12", "#,##0", ""),
    ("TOTAL ARR (Rs lakh)", "=B13/100000", "=C13/100000", "#,##0.0", ""),
    ("", "", "", "", ""),
    ("AI + infra cost (Rs/yr)", f"=B8*{AICOST}*12", f"=C8*{AICOST}*12", "#,##0",
     "Assumes the response cache is built"),
    ("Gross profit before content & salaries (Rs)", "=B13-B16", "=C13-C16", "#,##0", ""),
    ("Gross margin", "=B17/B13", "=C17/C13", "0.0%", "Before content, salaries and sales cost"),
]

r = 4
for label, f12, f24, fmt, note in lines:
    if label == "":
        r += 1
        continue
    lc = ws.cell(row=r, column=1, value=label)
    v1 = ws.cell(row=r, column=2, value=f12)
    v2 = ws.cell(row=r, column=3, value=f24)
    v1.number_format = fmt
    v2.number_format = fmt
    nc = ws.cell(row=r, column=4, value=note)
    nc.font = SMALL
    nc.alignment = WRAP
    if label.isupper() or label.startswith("TOTAL") or label.startswith("Gross"):
        lc.font = BOLD
        v1.font = BOLD
        v2.font = BOLD
        v1.fill = FILL_GREEN
        v2.fill = FILL_GREEN
    else:
        lc.font = BODY
        v1.font = BODY
        v2.font = BODY
        v1.fill = FILL_GREY
        v2.fill = FILL_GREY
    for col in range(1, 5):
        ws.cell(row=r, column=col).border = BOX
    r += 1

ws.freeze_panes = "A4"

# ======================================================== 5. UNIT ECONOMICS
ws = wb.create_sheet("Unit Economics")
title(ws, "Unit economics — B2B2C vs B2C direct", 4)
header(ws, 3, ["Metric", "B2B2C (institute)", "B2C direct", "Note"], [42, 20, 20, 46])

CAC_I = P["CAC per student — institute channel (Rs)"]
CAC_B = P["CAC per student — B2C direct (Rs)"]
RET_I = P["Annual retention — institute channel"]
RET_B = P["Annual retention — B2C direct"]

ue = [
    ("Revenue per student per year (Rs)", f"={SEAT}*12", f"={B2CP}", "#,##0",
     "Institute figure excludes the platform fee"),
    ("AI + infra cost per student per year (Rs)", f"={AICOST}*12", f"={AICOST}*12", "#,##0", ""),
    ("Gross profit per student per year (Rs)", "=B4-B5", "=C4-C5", "#,##0", ""),
    ("Gross margin", "=B6/B4", "=C6/C4", "0.0%", ""),
    ("", "", "", "", ""),
    ("CAC per student (Rs)", f"={CAC_I}", f"={CAC_B}", "#,##0",
     "Marketing/sales spend only — excludes founder and salaried sales time, which "
     "flatters the institute column"),
    ("Payback period (months)", "=B9/(B6/12)", "=C9/(C6/12)", "0.0", "CAC / monthly gross profit"),
    ("", "", "", "", ""),
    ("Annual retention", f"={RET_I}", f"={RET_B}", "0.0%", ""),
    ("Avg customer lifetime (years)", "=1/(1-B12)", "=1/(1-C12)", "0.0", ""),
    ("LTV (Rs)", "=B6*B13", "=C6*C13", "#,##0", "Gross profit x lifetime"),
    ("LTV : CAC ratio", "=B14/B9", "=C14/C9", "0.0", "Above 3.0 is healthy"),
]

r = 4
for label, b, c, fmt, note in ue:
    if label == "":
        r += 1
        continue
    lc = ws.cell(row=r, column=1, value=label)
    v1 = ws.cell(row=r, column=2, value=b)
    v2 = ws.cell(row=r, column=3, value=c)
    v1.number_format = fmt
    v2.number_format = fmt
    nc = ws.cell(row=r, column=4, value=note)
    nc.font = SMALL
    nc.alignment = WRAP
    hot = label.startswith(("Payback", "LTV", "Gross margin"))
    lc.font = BOLD if hot else BODY
    for v in (v1, v2):
        v.font = BOLD if hot else BODY
        v.fill = FILL_GREEN if hot else FILL_GREY
    for col in range(1, 5):
        ws.cell(row=r, column=col).border = BOX
    r += 1

ws.cell(row=r + 1, column=1,
        value="Read the Payback and LTV:CAC rows together — they are the whole argument "
              "for selling to institutes before selling to parents.").font = SMALL
ws.cell(row=r + 2, column=1,
        value="The institute LTV:CAC looks very high because CAC here counts marketing spend "
              "only. Add a salesperson's salary and it lands nearer 4-6 — still comfortably "
              "ahead of the B2C column, which is the point.").font = SMALL
ws.freeze_panes = "A4"

# ========================================================== 6. PUNE CEILING
ws = wb.create_sheet("Pune Ceiling")
title(ws, "What Pune alone maxes out at", 4)
header(ws, 3, ["Scenario", "Share of Pune SAM", "Paying students", "ARR (Rs crore)"], [34, 20, 20, 20])

r = 4
ws.cell(row=r, column=1, value="Blended revenue per student per year (Rs)").font = BODY
bc = ws.cell(row=r, column=2, value=f"={SEAT}*12*0.75+{B2CP}*0.25")
bc.number_format = "#,##0"
bc.fill = FILL_GREY
bc.font = BODY
ws.cell(row=r, column=3, value="75% institute-priced, 25% B2C-priced").font = SMALL
for col in range(1, 5):
    ws.cell(row=r, column=col).border = BOX

scen = [("Base — modest outcome", 0.05), ("Good outcome", 0.10),
        ("Strong outcome", 0.18), ("Dominant — near-ceiling", 0.25)]
r = 6
for name, share in scen:
    ws.cell(row=r, column=1, value=name).font = BODY
    sc = ws.cell(row=r, column=2, value=share)
    sc.number_format = "0.0%"
    sc.fill = FILL_INPUT
    sc.font = BOLD
    st = ws.cell(row=r, column=3, value="=%s*B%d" % (SAM_CELL, r))
    st.number_format = "#,##0"
    st.fill = FILL_GREY
    ar = ws.cell(row=r, column=4, value="=C%d*$B$4/10000000" % r)
    ar.number_format = "0.00"
    ar.fill = FILL_GREEN
    ar.font = BOLD
    for col in range(1, 5):
        ws.cell(row=r, column=col).border = BOX
    r += 1

r += 2
note = [
    "THE POINT OF THIS SHEET",
    "Even a dominant position in Pune caps the business at a few crore of ARR.",
    "Pune is the right beachhead and the wrong final market.",
    "",
    "Maharashtra SSC and HSC each draw roughly 14-16 lakh candidates per year statewide,",
    "against roughly 1.4 lakh SSC students in Grades 9-10 in all of Pune.",
    "Statewide is on the order of 20x the Pune opportunity — on identical content.",
    "",
    "That is the strongest argument for the SSC-first strategy: the content built for Pune",
    "is the same content that unlocks a market twenty times larger, with no rebuild.",
]
for line in note:
    c = ws.cell(row=r, column=1, value=line)
    c.font = Font(size=11, bold=True, color=NAVY) if line.isupper() and line else BODY
    r += 1

# ============================================================== 7. SOURCES
ws = wb.create_sheet("Sources")
title(ws, "Where to get the real numbers", 4)
header(ws, 3, ["Input to replace", "Source", "How", "Cost"], [34, 30, 62, 12])

src = [
    ("Students per grade, per board, Pune", "UDISE+ (udiseplus.gov.in)",
     "School-level enrolment, filterable to Pune district by board and grade. "
     "The single best source. Start here.", "Free"),
    ("Pune urban population, current", "Census 2011 + PMRDA / PMC projections",
     "Use the 2011 UA figure as the base and the corporation's own growth projection.", "Free"),
    ("SSC / HSC candidate counts", "MSBSHSE (mahahsscboard.in)",
     "Annual result press releases give exact appeared-candidate counts, district-wise.", "Free"),
    ("CBSE school count in Pune", "CBSE affiliated-school directory",
     "Filter the official list by district; multiply by average enrolment.", "Free"),
    ("ICSE / ISC school count", "CISCE school locator", "Same approach as CBSE.", "Free"),
    ("Coaching class count in Pune", "GST directory + Google Maps",
     "Maharashtra shops-and-establishment registrations; cross-check with a Maps count "
     "per locality. Rough, but enough to size the channel.", "Free / low"),
    ("Household spend on tuition", "NSSO Household Social Consumption: Education",
     "Gives urban Maharashtra spend per student on private coaching.", "Free"),
    ("Willingness to pay for digital", "Your own landing-page test",
     "A landing page plus about Rs 15,000 of targeted ads gives you the real conversion "
     "rate in a week. Cheaper and more honest than any survey.", "~Rs 15k"),
    ("Institute price acceptance", "15 coaching class visits",
     "Ask one question: would you pay Rs 90 per student per month for a test engine with "
     "weakness reports? Three yeses justifies the build.", "Free"),
]

r = 4
for a, b, c, d in src:
    ws.cell(row=r, column=1, value=a).font = BOLD
    ws.cell(row=r, column=2, value=b).font = BODY
    cc = ws.cell(row=r, column=3, value=c)
    cc.font = BODY
    cc.alignment = WRAP
    ws.cell(row=r, column=4, value=d).font = BODY
    for col in range(1, 5):
        ws.cell(row=r, column=col).border = BOX
        ws.cell(row=r, column=col).alignment = WRAP
    ws.row_dimensions[r].height = 42
    r += 1

ws.freeze_panes = "A4"

out = "/var/lib/freelancer/projects/40697081/SmartStudent-Pune-Market-Model.xlsx"
wb.save(out)
print("saved", out)
