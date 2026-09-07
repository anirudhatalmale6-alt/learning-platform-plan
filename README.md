# SmartStudent — development plan, viability assessment and Pune market model

Three questions were asked. One document each.

| # | Document | Question it answers |
|---|---|---|
| 1 | [Development plan](01-DEVELOPMENT-PLAN.md) | How would this actually get built? |
| 2 | [Is it worth building?](02-IS-IT-WORTH-BUILDING.md) | Should it be built at all? |
| 3 | [Pune market opportunity](03-MARKET-OPPORTUNITY-PUNE.md) | How big is the opportunity in Pune alone? |
| — | `SmartStudent-Pune-Market-Model.xlsx` | The sizing model as a live spreadsheet |

---

## The short version

**Build it — but not the product in the brief.**

The brief describes four boards × six grades × all subjects, sold to parents. That
is roughly 168 board-grade-subject units, a 20–24 month build, and a head-on fight
with companies that raised hundreds of crores and mostly lost.

The version worth building is narrower:

> **Maharashtra SSC, Grades 9–10, Maths + Science first. Sold to Pune coaching
> classes and schools, not directly to parents. AI diagnostic + concept-scoped
> tutor + institute test engine.**

Reasons, in order of weight:

1. **SSC is the one board where you can be the best product available.** Every
   funded national player optimises for CBSE, JEE and NEET. SSC-pattern content in
   Marathi medium is thin and dated.
2. **The content is the cost, not the code.** The platform is ~25% of the effort.
   Building four boards at once guarantees being shallow in all four.
3. **Institutes are a better customer than parents.** One sale brings 100+
   students, payback is ~3 months instead of ~7, and retention is roughly double.
4. **Assume every student already has a free AI chatbot.** The product must be
   worth paying for *given that* — which means persistent per-concept mastery,
   strict syllabus scoping, real board-blueprint mocks, and parent/teacher
   reporting. Those are things a general chatbot structurally cannot do.
5. **Pune is a beachhead, not a business.** Even a dominant Pune position caps out
   near ₹3.7 crore ARR. Statewide Maharashtra SSC is roughly 20x larger — on
   identical content.

Timeline: **~12 weeks to something sellable**, ~26 weeks to something defensible.

---

## About the numbers

Every figure in the market documents is a **modelled estimate, not a researched
fact**, and each is labelled with a confidence level and the specific source to
check it against. The derivations are all visible so you can see which assumption
drives which output.

The spreadsheet is the real deliverable there — every yellow cell is an input, and
everything else is a live formula. Change an assumption and the whole model moves.

**Before spending money on the build:** UDISE+ (`udiseplus.gov.in`) publishes
school-level enrolment for Pune district by board and grade, for free. About a
day's work there replaces the entire top half of the model with hard data.

---

## Two things flagged early because they get expensive late

- **IGCSE and ICSE past papers are rights-protected.** Cambridge and CISCE both
  license their papers; you cannot reproduce them in a commercial product without
  permission. This is a concrete reason to sequence those boards last. NCERT is
  the most permissive, which is part of why CBSE is the cheap second board.
- **Your users are minors, so the DPDP Act applies.** Verifiable parental consent
  is required, and behavioural tracking of children is prohibited. Build the
  parent-linked account model in at Phase 0 — retrofitting consent flows across an
  existing user base is genuinely painful.

Neither of these is legal advice, but both are checkable, and both should be
verified before the content budget is committed.
</content>
</invoke>
