# Market opportunity — Pune City only

## Read this first

**Every number below is a modelled estimate, not a researched fact.** I have shown
the full derivation for each so you can see exactly which assumption drives which
output, and I have named the specific source to check for each input. Do not put
these figures in an investor deck until the inputs marked ⚠️ have been replaced
with real data.

I am deliberately not quoting confident-sounding statistics I cannot stand behind.
A sizing model whose assumptions are visible and checkable is more useful to you
than a set of impressive numbers with invisible origins.

The accompanying spreadsheet (`SmartStudent-Pune-Market-Model.xlsx`) has all of
this as live formulas — change any assumption in the yellow cells and every figure
downstream updates. That is the actual deliverable here; this document explains it.

---

## 1. Sources to validate the inputs

| Input | Where to get the real number | Cost |
|---|---|---|
| Students per grade, per board, in Pune | **UDISE+** (`udiseplus.gov.in`) — school-level data, filterable to Pune district, by board and grade. This is the single best source and it is free. | Free |
| Pune urban population, current | Census 2011 as base + Pune Municipal Corporation / PMRDA projections | Free |
| SSC/HSC candidate counts | MSBSHSE (`mahahsscboard.in`) annual result press releases give exact appeared-candidate counts, district-wise | Free |
| CBSE school count in Pune | CBSE affiliated-school directory, filter by district | Free |
| ICSE/ISC school count | CISCE school locator | Free |
| Coaching class count | Maharashtra shops-and-establishment registrations, GST directory, Justdial/Google Maps counts as a rough cross-check | Free / low |
| Household spend on tuition | NSSO Household Social Consumption: Education survey | Free |

**A day of work in UDISE+ replaces the entire top half of this model with real
numbers.** I strongly recommend doing that before committing budget.

---

## 2. Funnel: TAM → SAM → SOM (Pune only)

### Layer 1 — Total students, Grades 7–12, Pune urban

| Step | Value | Basis |
|---|---|---|
| Pune urban agglomeration population, 2026 | ⚠️ ~7.4 million | Census 2011 UA was ~5.05M; extrapolated at ~2.7%/yr. **Verify against PMRDA projections.** |
| Share aged 12–17 | ⚠️ ~9.5% | Urban India age structure; urban metros run below the national ~11% because of lower fertility. **Verify against Census age tables.** |
| **Students in the Grade 7–12 band** | **≈ 703,000** | |
| Of whom enrolled in school | ~96% (urban) | |
| **TAM (students)** | **≈ 675,000** | |

### Layer 2 — Board split

⚠️ This split is an estimate based on the general pattern of Maharashtra metros.
**UDISE+ gives you the exact figure — replace this.**

| Board | Est. share | Students | Notes |
|---|---|---|---|
| Maharashtra SSC/HSC | ~60% | ~405,000 | Your beachhead. Marathi + English medium. |
| CBSE | ~24% | ~162,000 | Higher spend, more competition |
| ICSE/ISC | ~9% | ~61,000 | Highest spend per student, small |
| IGCSE / IB | ~2% | ~13,500 | Very small, worst licensing position |
| Other | ~5% | ~34,000 | |

### Layer 3 — SAM: who can actually be sold to

Filters applied to the 675,000:

| Filter | Retained | Running total |
|---|---|---|
| Has smartphone + data access at home | ~88% | 594,000 |
| Household already pays for supplementary learning (tuition/coaching/books) | ⚠️ ~55% | 327,000 |
| Willing to pay for a *digital* product specifically | ⚠️ ~35% of the above | **≈ 114,000** |

**SAM ≈ 114,000 students in Pune.**

The third filter is the one I am least confident in and the one that matters most.
It is also the easiest to test cheaply: a landing page and ₹15,000 of targeted
ads will tell you the real conversion rate in a week.

### Layer 4 — SOM: realistically winnable

Restricting to the wedge (SSC, Grades 9–10, via institutes):

| Step | Value |
|---|---|
| SSC students in Pune | ~405,000 |
| In Grades 9–10 (2 of 6 grades, weighted slightly up for board-year focus) | ~146,000 |
| Reachable through coaching classes / schools | ⚠️ ~60% → 87,500 |
| Realistic share won in 24 months | ⚠️ 4–7% |
| **SOM, month 24** | **≈ 3,500 – 6,100 paying students** |

---

## 3. Revenue model

Three streams. The institute stream is the one that should carry the business.

| Stream | Price | Who pays | Notes |
|---|---|---|---|
| **Institute seat** | ₹90/student/month, 50-seat minimum | Coaching class / school | Primary. Annual contract, billed to the institute. |
| **Institute platform fee** | ₹6,000/month flat | Institute | Test engine, batches, analytics, branding |
| **B2C direct** | ₹249/month or ₹1,999/year | Parent | Secondary. Do not run paid ads for this in year 1. |

### Pune-only revenue projection

| | Month 12 | Month 24 |
|---|---|---|
| Institutes signed | 12 | 40 |
| Avg paying students per institute | 110 | 130 |
| Students via institutes | 1,320 | 5,200 |
| B2C direct students | 400 | 1,800 |
| **Total paying students** | **1,720** | **7,000** |
| Institute seat revenue/yr | ₹14.3 L | ₹56.2 L |
| Institute platform fees/yr | ₹8.6 L | ₹28.8 L |
| B2C revenue/yr | ₹8.0 L | ₹36.0 L |
| **ARR** | **≈ ₹31 lakh** | **≈ ₹121 lakh (₹1.21 cr)** |

### The Pune ceiling — the important finding

If you eventually captured **10% of the entire Pune SAM** — about 11,400 students,
which would be an excellent outcome — at a blended ₹1,310/student/year, Pune alone
produces roughly **₹1.5 crore ARR**. Pushing to a very strong 25% of SAM, about
28,600 students, gets you to roughly **₹3.7 crore**.

**So: Pune is a beachhead, not a business.** It is the right place to start — it is
where you are, the SSC content is reusable statewide, and 40 reference customers in
one city is a credible proof point. But the model has to plan for Maharashtra-wide
SSC expansion from month 18, because that is where the actual scale is: the state's
SSC and HSC cohorts are each in the range of 14–16 lakh candidates a year, versus
roughly 145,000 SSC students in grades 9–10 in all of Pune. **Statewide is
approximately 20x the Pune opportunity, on identical content.**

That is the strongest argument for the SSC-first strategy: the content you build
for Pune is the same content that unlocks a market twenty times larger, with no
rebuild.

---

## 4. Unit economics

| Metric | B2B2C (institute) | B2C direct |
|---|---|---|
| Revenue per student/year | ₹1,080 + platform fee share | ₹1,999 |
| CAC per student | ⚠️ ₹120–250 | ⚠️ ₹700–1,400 |
| AI + infra cost/student/year | ₹280–400 | ₹280–400 |
| Content amortisation/student | falls with scale | falls with scale |
| Gross margin | ~65–72% | ~55–65% |
| Annual retention | ⚠️ ~70% (institute renews in bulk) | ⚠️ ~30–40% |
| **Payback period** | **~3 months** | **~10 months** |

This table is the whole argument for the B2B2C-first strategy in one place. The
B2C column is not disastrous, but it needs working capital you probably do not
want to raise, and its retention is the weak point — a parent who stops seeing
value cancels in month 3, whereas an institute renews the whole batch annually.

---

## 5. Competitive picture in Pune

| Competitor | Strength | Gap you can exploit |
|---|---|---|
| Physics Wallah | Price, brand, JEE/NEET | Thin on SSC-pattern board prep, no institute tooling |
| BYJU'S | Brand recall (now negative) | Distressed, no institute product |
| Vedantu / Unacademy | Live classes | Not a practice/diagnostic engine, not SSC-focused |
| Khan Academy / DIKSHA | Free, credible | No board-pattern testing, no analytics, no institute layer |
| ChatGPT / Gemini free tier | Excellent doubt-solving, free | **No persistent mastery state, no syllabus scoping, no parent report, no institute layer** |
| Local Marathi SSC apps | Language, price | Usually PDF dumps; dated UX, no adaptivity |

The row that matters is the free chatbot row. **Assume every one of your students
already has one.** The product must be valuable *given that*, which means the value
has to sit in the things a general chatbot structurally cannot do: knowing what
this specific student has and has not mastered, scoping strictly to their board's
syllabus depth, running real board-blueprint mock papers, and reporting to the
parent and the teacher.

---

## 6. Go-to-market for Pune, first 6 months

1. **Weeks 1–2 — validate before building.** Visit 15 coaching classes in Kothrud,
   Sadashiv Peth, Pimpri and Wakad. One question: *"if I gave you a test engine
   with per-student weakness reports for your SSC batch, would you pay ₹90 per
   student per month?"* Three yeses justifies the build.
2. **Weeks 3–12 — build Phases 0–2** against two named design partners who get it
   free in exchange for weekly feedback and a testimonial.
3. **Weeks 13–20 — paid pilots.** Convert the design partners plus 8 more. Charge
   from day one, even if discounted — free pilots do not tell you anything about
   willingness to pay.
4. **Weeks 21–26 — proof and referral.** Publish real outcome data from the pilot
   batches. Coaching class owners in Pune talk to each other constantly; a
   referral incentive works better here than any ad spend.
5. **Only after 20 paying institutes — open B2C.** By then you have content depth,
   testimonials, and known unit economics.

**Do not spend on paid consumer acquisition in year 1.** Against PW's pricing and
brand, it will not pay back.

---

## 7. Summary

- **TAM (Pune, Grades 7–12):** ~675,000 students
- **SAM (can and will pay for digital):** ~114,000 students
- **SOM (24 months, SSC 9–10 wedge):** ~3,500–6,100 paying students
- **Realistic ARR at month 24, Pune only:** ~₹1.2 crore
- **Pune-only ceiling at a strong outcome:** ~₹1.5–3.7 crore ARR
- **Maharashtra-wide, same content:** roughly 20x the Pune opportunity

**Pune is the right beachhead and the wrong final market.** Build for Pune, but
build the content and the schema so that month 18 is a distribution problem rather
than a rebuild.
</content>
</invoke>
