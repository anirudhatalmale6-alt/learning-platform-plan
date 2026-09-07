# SmartStudent — Full Development Plan

---

## A. Scope definition

### A1. The content graph (the core of the product)

```
Board
 └─ Grade (7–12)
     └─ Subject
         └─ Chapter            (maps 1:1 to the textbook chapter)
             └─ Topic          (a section within the chapter)
                 └─ Concept    (the smallest testable idea — the atom)
                     └─ Question
```

The **Concept** node is the unit that makes this product different from a PDF
question bank. Everything hangs off it:

- a student's mastery score is stored per concept, not per chapter
- a wrong answer maps back to the concept, not the question
- prerequisites are concept→concept edges (this is what lets the system say
  *"you failed this trigonometry question because you never learned similar
  triangles in Grade 9"*)
- AI explanations are generated with the concept as context, which is what stops
  the model wandering off-syllabus

This means the graph is not a tree — it is a **DAG**. Concepts have prerequisite
edges that cross chapters, grades, and sometimes boards. That single design
decision drives most of the schema below.

### A2. Board coverage — phased, not all at once

| Priority | Board | Reason |
|---|---|---|
| 1 | Maharashtra SSC/HSC | Underserved, local, Pune-native, weakest competition |
| 2 | CBSE | Largest cohort, NCERT content is the most reusable |
| 3 | ICSE/ISC | Smaller, English-medium, higher willingness to pay |
| 4 | IGCSE | Smallest cohort, worst content licensing position |

---

## B. Data model

Core tables (PostgreSQL). Written out because this is the part most implementations
get wrong and cannot fix later.

```sql
-- ============ CURRICULUM SPINE ============

boards          (id, code, name, region, language_default)
grades          (id, board_id, number, label)             -- 7..12
subjects        (id, board_id, grade_id, code, name, stream)
                                                          -- stream: NULL | science | commerce | arts
chapters        (id, subject_id, seq, name, textbook_ref, weightage_pct)
topics          (id, chapter_id, seq, name)

concepts        (id, topic_id, seq, name, slug,
                 bloom_level,            -- remember|understand|apply|analyse|evaluate|create
                 difficulty_band,        -- 1..5
                 est_minutes,
                 canonical_concept_id)   -- cross-board dedupe: "Pythagoras" is one idea
                                         -- taught by all 4 boards

concept_prereq  (concept_id, prereq_concept_id, strength)  -- the DAG edges

-- ============ ASSESSMENT ============

questions       (id, concept_id, type, stem, solution, difficulty,
                 marks, expected_seconds, source_type, source_ref,
                 language, status, authored_by, reviewed_by)
                 -- type: mcq_single | mcq_multi | numeric | short | long |
                 --       assertion_reason | match | diagram
                 -- source_type: original | pyq | textbook_exercise
                 -- status: draft | ai_generated | in_review | approved | retired

question_options(id, question_id, seq, body, is_correct, misconception_id)
misconceptions  (id, concept_id, name, description)
                 -- WHY a distractor is wrong. This is what turns a wrong answer
                 -- into a diagnosis instead of just a red X.

question_assets (id, question_id, kind, url, alt_text)     -- diagrams, graphs
question_i18n   (question_id, language, stem, solution)    -- en | mr | hi

papers          (id, board_id, grade_id, subject_id, year, session, blueprint)
paper_questions (paper_id, question_id, q_number, section)

-- ============ LEARNER ============

users           (id, role, phone, email, name, created_at)
                 -- role: student | parent | teacher | institute_admin | content_admin
students        (user_id, board_id, grade_id, medium, school_id, stream)
parent_links    (parent_user_id, student_user_id, relation, verified_at)
institutes      (id, name, type, city, plan, seats)       -- schools + coaching classes
institute_users (institute_id, user_id, role)
batches         (id, institute_id, name, board_id, grade_id, teacher_user_id)
batch_members   (batch_id, student_user_id)

attempts        (id, student_id, question_id, session_id,
                 response, is_correct, seconds_taken, confidence,
                 hint_used, attempted_at)

mastery         (student_id, concept_id, theta, attempts_n, last_seen_at,
                 next_review_at, retention_score)
                 -- theta = IRT ability estimate, updated per attempt

test_sessions   (id, student_id, kind, blueprint_id, started_at,
                 submitted_at, score, percentile)
                 -- kind: practice | chapter_test | mock_paper | diagnostic

-- ============ AI LAYER ============

ai_conversations(id, student_id, concept_id, started_at)
ai_messages     (id, conversation_id, role, content, tokens_in, tokens_out,
                 model, cost_paise, flagged)
ai_cache        (prompt_hash, concept_id, language, response, hits, created_at)
                 -- critical for unit economics; see section F
```

### Why `canonical_concept_id` matters

"Laws of Motion" appears in CBSE Grade 9, SSC Grade 9, ICSE Grade 9 and IGCSE. The
underlying physics is identical; the depth, notation and paper pattern differ.
Mapping all four to one canonical concept means:

- one set of explanations and diagrams, reused four times
- questions can be *promoted* between boards after a review pass
- content cost drops by an estimated 35–50% once you are on your third board

Skipping this is the single most expensive mistake possible here. Retrofitting it
after 100k questions exist is effectively a rebuild.

---

## C. AI layer — what it does, concretely

"AI-powered" has to mean specific mechanisms, otherwise it is a marketing word.
Five features, in order of how much they matter:

### C1. Diagnostic placement (highest value, cheapest to build)
A 20-question adaptive test locates a student on the concept DAG and finds the
*earliest* unmastered prerequisite. Output: "you are being taught Grade 10
quadratics, but your actual gap is Grade 8 factorisation." No competitor at this
price point does this well and it is the single most convincing demo for a parent.
Uses IRT + the prereq graph. **No LLM needed** — this is maths, so it costs nothing
per use.

### C2. Concept-scoped doubt solving
A chat tutor that is *constrained to the concept node* the student is on — the
retrieval context is that concept's explanation, its worked examples, its
prerequisites, and the board's syllabus depth for that grade. This is what stops
it giving a Grade 12 answer to a Grade 9 SSC student, which is exactly what the
free chatbots do.

Guardrails required from day one:
- refuse to give the final answer to a question inside an active graded test
- Socratic mode by default (hint ladder: nudge → method → worked example → answer)
- every response tagged with the concept, so parent/teacher reporting works
- content safety filter on both directions

### C3. Question generation with human review
AI drafts variants from an approved seed question — same concept, same difficulty
band, different numbers/context. Every generated item goes to `status =
ai_generated` and **a human teacher approves before it ever reaches a student.**
This is non-negotiable: an unreviewed AI question bank in an exam-prep product is
a reputational time bomb, especially in Maths and Science where the model will
produce a confidently wrong solution roughly 3–8% of the time.

Realistic economics: AI drafting takes review time from ~12 min/question to
~3 min/question. That is the real ROI — a 4x content throughput multiplier, not
free content.

### C4. Answer evaluation for written responses
Grading short/long answers against a board-style marking rubric, awarding partial
marks step-by-step the way an SSC/HSC examiner does. High value for board prep,
genuinely hard to get right, so build it after C1–C3 are stable.

### C5. Spaced repetition + weakness reports
Scheduling revision against `mastery.next_review_at`, and a weekly parent report:
"3 weak concepts, here they are, here is what to practise." The parent report is
what drives renewal — the student uses it, the parent pays for it.

---

## D. Architecture

```
                       ┌──────────────────────────┐
   Student (mobile web)│                          │
   Parent (mobile web) ├──► CDN ──► Next.js app   │
   Teacher (desktop)   │           (SSR + PWA)    │
                       └──────────┬───────────────┘
                                  │  REST/tRPC
                       ┌──────────▼───────────────┐
                       │   API — NestJS / FastAPI │
                       ├──────────────────────────┤
                       │ auth  content  assessment│
                       │ mastery  reporting  billing
                       └───┬───────┬──────────┬───┘
                           │       │          │
              ┌────────────▼──┐ ┌──▼────────┐ ┌▼──────────────┐
              │ PostgreSQL    │ │  Redis    │ │ Worker queue  │
              │ (content DAG, │ │ (session, │ │ (BullMQ)      │
              │  attempts,    │ │  AI cache)│ │ – AI gen      │
              │  mastery)     │ └───────────┘ │ – grading     │
              └───────────────┘               │ – reports     │
                                              │ – PDF export  │
              ┌───────────────┐               └───┬───────────┘
              │ Object store  │                   │
              │ (S3/R2)       │◄──────────────────┤
              │ diagrams, PDF │                   │
              └───────────────┘         ┌─────────▼──────────┐
                                        │  AI Gateway        │
                                        │  – prompt registry │
                                        │  – cache lookup    │
                                        │  – cost ledger     │
                                        │  – model router    │
                                        └─────────┬──────────┘
                                                  │
                                        Claude / GPT / local
```

**The AI Gateway is a required component, not an optimisation.** Every model call
goes through it so that: prompts are versioned, responses are cached by
(concept, language, prompt-hash), per-student cost is metered, and the model can be
swapped without touching feature code. Without it you cannot answer "what does a
student cost us per month", which is the number the whole business rests on.

### Stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | Next.js + React, PWA | One codebase, installable, works on low-end Android. Native apps later, only if retention justifies it. |
| Styling | Tailwind | Fast, consistent, easy handover |
| API | NestJS (TS) or FastAPI (Python) | TS if one team owns both ends; Python if the ML/IRT work grows |
| DB | PostgreSQL 16 | Recursive CTEs handle the prereq DAG natively |
| Cache/queue | Redis + BullMQ | |
| Search | Postgres FTS first, Meilisearch when it hurts | Don't add Elasticsearch on day one |
| Storage | Cloudflare R2 | No egress fees — matters when serving diagrams to 10k students |
| Video | Bunny.net or Cloudflare Stream | Cheaper than Mux at Indian volumes |
| Payments | Razorpay | UPI + autopay mandates; essential for Indian subscription retention |
| SMS/OTP | MSG91 | |
| Hosting | India region (ap-south-1 / Mumbai) | Latency + data residency under the DPDP Act |
| Analytics | PostHog (self-hosted) | Product analytics without per-event billing |

### Non-negotiable engineering constraints for this market

1. **Mobile-first, low-end Android.** Target a ₹8,000 phone on 4G, not an iPhone.
   Budget: <200KB initial JS, usable at 3G speeds.
2. **Offline practice.** Downloadable question sets + attempts that sync later.
   Connectivity in parts of the Pune belt is inconsistent and this is a top-3
   churn cause.
3. **Marathi from the schema up.** `question_i18n` exists from day one even if only
   English is populated. Bolting on a second language later means touching every
   query.
4. **Exam-realistic rendering.** LaTeX maths, chemistry notation, and diagrams must
   render exactly as the board prints them. Students distrust a paper that looks
   different from their textbook, and this is a top-3 reason for abandonment.

---

## E. Phased delivery plan

Each phase ends with something demoable and, from Phase 2 on, sellable.

### Phase 0 — Foundations (Weeks 1–3)
- Repo, CI, staging environment, auth (phone + OTP), role model
- Full schema migration, seeded with **one** complete subject:
  SSC Grade 10 Mathematics Part 1, mapped to Concept level
- Admin content console: create/edit the Board→…→Concept tree, import questions
- **Exit:** an admin can build the full tree for one subject and see it rendered

### Phase 1 — Practice engine (Weeks 4–7)
- Question renderer (all 8 question types, LaTeX, diagrams)
- Practice sessions, attempt recording, immediate feedback with worked solution
- Mastery scoring per concept (IRT), concept mastery dashboard
- Diagnostic placement test (feature C1)
- **Exit:** a real student can be placed and practise a full chapter. This is the
  first thing to demo to a coaching class.

### Phase 2 — Tests & the AI tutor (Weeks 8–12)
- Chapter tests + full mock papers with board blueprints and real timing
- Auto-grading (objective + numeric), OMR-style review screen
- AI doubt-solver with concept scoping and hint ladder (C2)
- AI Gateway with caching and per-student cost metering
- **Exit:** first paid pilot with 2–3 Pune coaching classes

### Phase 3 — Institute layer (Weeks 13–17)
- Institute/teacher accounts, batches, bulk student onboarding
- Assign tests to a batch, live monitoring, class-level analytics
- Teacher-facing weakness heatmap (concept × student grid)
- Parent portal + weekly report (C5)
- Razorpay subscriptions, UPI autopay, institute invoicing
- **Exit:** an institute can run its whole test cycle on the platform — this is
  the point where it becomes hard for them to leave

### Phase 4 — Content scale-up (Weeks 14–26, runs in parallel)
- AI-assisted question generation + review workflow (C3)
- Written-answer evaluation (C4)
- Expand: SSC 9–10 all Science/Maths → CBSE 9–10 → SSC 11–12 → ICSE
- Target at exit: ~35,000 reviewed questions across the priority boards

### Phase 5 — Retention & growth (Weeks 27+)
- Spaced repetition scheduler, streaks, leaderboards (batch-scoped, not global —
  global leaderboards demotivate the bottom 70%)
- Referral mechanics, school reporting exports
- Regional expansion: rest of Maharashtra, then ICSE/IGCSE metros

**Realistic timeline to a revenue-generating product: ~12 weeks (end of Phase 2).
To a defensible one: ~26 weeks.** The brief's full scope is 20–24 months.

---

## F. Cost structure — the number that decides everything

### Per-student monthly AI cost

The failure mode of every AI edtech product is an unbounded chat feature. A heavy
student can burn more in model calls than they pay in subscription.

| Item | Assumption | Cost/student/month |
|---|---|---|
| Doubt-solver messages | 40 msgs, ~1,200 tok in / 500 out | ₹18–35 |
| Cache hit rate | 45% (same concepts, same doubts, repeatedly) | −45% |
| Answer evaluation | 20 written answers | ₹8–14 |
| **Net** | | **₹18–32** |

Against a ₹200–400/month price point this is workable, but only with:
- the response cache (identical doubts on identical concepts repeat constantly)
- a fair-use cap (e.g. 60 AI messages/month on the base tier)
- a cheaper model for routine work, the strong model only for evaluation and
  generation

Without the gateway and cache, expect ₹60–120/student/month and a broken margin.

### Build cost, phased

| Phase | Effort | Notes |
|---|---|---|
| 0–1 | ~7 weeks | Platform + practice engine |
| 2 | ~5 weeks | Tests + AI tutor |
| 3 | ~5 weeks | Institute layer + billing |
| 4 | continuous | Content — the dominant ongoing cost |

Content is the real budget line: at ~₹10/question all-in for AI-drafted +
teacher-reviewed items, 35,000 questions ≈ ₹3.5 lakh, plus 2–3 part-time subject
teachers for review. Budget content as its own P&L line, separate from
engineering — treating it as "we'll fill it in later" is how these platforms end
up as an empty shell with a good UI.

---

## G. Legal and compliance — flagging early, because these bite late

1. **IGCSE past papers are strictly licensed by Cambridge.** You cannot reproduce
   Cambridge past papers in a commercial product without permission. This is a
   concrete reason to put IGCSE last, or to use only originally-authored items
   for it.
2. **ICSE/CISCE past papers** are similarly rights-protected. Original items
   *aligned to* the pattern are fine; reproductions are not.
3. **NCERT** is the most permissive of the four and is the reason CBSE is cheap to
   cover. Still check the current terms before bulk reproduction.
4. **Maharashtra State Board (Balbharati)** textbook content — verify reproduction
   terms. Syllabus *structure* is a fact and not protectable; the text and figures
   are.
5. **DPDP Act 2023 + children's data.** Your users are minors. Verifiable parental
   consent is required for under-18s, and behavioural advertising and tracking of
   children is prohibited. This shapes onboarding: a student account must be
   linked to a verified parent. Build it in at Phase 0 — retrofitting consent
   flows across an existing user base is genuinely painful.
6. **AI output disclaimers.** State plainly that AI explanations are a study aid
   and that graded content is teacher-reviewed. Keep the review audit trail
   (`reviewed_by`, timestamps) — it is your defence if a wrong solution surfaces.

I am not a lawyer and none of the above is legal advice — but each of these is a
real, checkable item, and items 1, 2 and 5 should be verified with a lawyer before
Phase 4 spending starts.

---

## H. What I would build first, if you want one thing

If the budget only allows one deliverable to test the market: **the diagnostic
placement test for SSC Grade 10 Maths.** One subject, 20 adaptive questions, and a
report that names the exact prerequisite gaps. It demos in 4 minutes, it is the
thing coaching class owners react to, and it requires ~600 questions rather than
600,000.
</content>
</invoke>
