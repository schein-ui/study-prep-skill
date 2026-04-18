# Deliverable Roles

Each deliverable has a distinct pedagogical role and a specific study-plan slot. Knowing the role prevents over-producing.

## Standalone interactive HTML — the primary study artifact

**Role:** Main reading surface. This is what the student opens 80% of the time.

**Used when:** Day 1 comprehension pass; Day 2 reference while quizzing; any time a question comes up.

**Format constraint:** Single .html file. All SVGs inlined. No framework. Works offline on any device.

**Distinguishing feature:** Interactive. Click-to-reveal quiz. Nav sidebar with urgent "Errors in My Notes" tab. Mobile responsive.

**When it's NOT the right tool:** Test morning. The student shouldn't be scrolling through the full guide on test day. Use the cheat sheet.

## Cheat sheet — 2-page print PDF

**Role:** Test-morning scan. 15 minutes, once, then stop.

**Used when:** Morning of the test. Nothing else is appropriate in this slot.

**Format constraint:** Fits on exactly 2 printed letter pages. Visual-dense. Color-coded by subtopic.

**Distinguishing feature:** Zero new content. Everything on the cheat sheet must also be in the study guide. This is a recall prompt, not a teaching document.

**When it's NOT the right tool:** Day 1, 2, or 3. The cheat sheet is compressed — studying it early skips the comprehension phase.

## Glossary — canonical source of truth

**Role:** Reference document that every other deliverable defers to.

**Used when:** Student hits a term they don't know. They look it up here.

**Format constraint:** Plain term → definition. No narrative. One definition per term (no conflicting versions).

**Distinguishing feature:** Every term matches the teacher's primary-source definition, and every look-alike trap (terms the student confused in homework) has its own entry in a dedicated trap-list.

**When it's NOT the right tool:** As study material. Glossaries are references, not study plans. Don't tell the student to "read the glossary" as a session.

## Quiz bank — active-recall practice

**Role:** Diagnostic — find out what the student doesn't know.

**Used when:** Day 2 of the study plan. After comprehension, before the cheat sheet.

**Format constraint:** MC with 4 options; at least one distractor per question built from the student's actual errors. SA and FRQ include scoring targets.

**Distinguishing feature:** The distractors are the teaching moment. When the student picks a wrong option that matches their own prior error, the explanation connects: "this is what you wrote in your reading guide, and here's why it's wrong."

**When it's NOT the right tool:** Day 1. Quizzing before comprehension produces frustration, not learning.

## Study plan — the schedule

**Role:** Tells the student what to do each day.

**Used when:** Day 0 (set the pace). Then referenced at the start of each day.

**Format constraint:** Specific activities with minute estimates. "Study Ch 17 for 30 minutes" is wrong; "Read the evidence-for-evolution section, then answer retrieval-practice Q1-5 without looking" is right.

**Distinguishing feature:** Explicit rules (retrieval > rereading, interleaving, sleep over cramming). The student is unlikely to know these instinctively.

**When it's NOT the right tool:** As standalone content. It's a meta-document.

## Flashcards — spaced repetition on phone

**Role:** Commute / idle-time / bed-time study. The only deliverable designed for a phone.

**Used when:** Anytime the student has 5-10 spare minutes.

**Format constraint:** Tab-separated plain text. Quizlet-compatible import. Split into Must-Know and Should-Know.

**Distinguishing feature:** Works on devices where the study guide HTML doesn't feel right (e.g., on the bus). Audio review via Quizlet's "Listen" feature is a bonus for auditory learners.

**When it's NOT the right tool:** For FRQ or diagram practice. Flashcards are for recall-level knowledge, not application.

## SVG visuals — dual-coded reinforcement

**Role:** Visual encoding of concepts that text alone encodes weakly.

**Used when:** Embedded in the study guide (throughout) and called out in the quiz bank (diagram questions).

**Format constraint:** `<svg viewBox="..."><text>...</text></svg>` — text as actual text elements, not paths. Labels everything. Short caption if not self-evident.

**Distinguishing feature:** When there's a teacher-specific figure (a specific cladogram, a specific graph from a specific slide), reproduce the teacher's exact version — not a textbook-generic version. The teacher's specific figure is what will be tested.

**When it's NOT the right tool:** For purely verbal content. Don't force a diagram where prose is clearer.

## QC report — process artifact for the parent

**Role:** Parent review. Demonstrates what was verified, what wasn't, where gaps exist.

**Used when:** Parent wants to double-check before handing the bundle to the student.

**Format constraint:** Specific evidence — "verified X against Y page N." Not vague claims.

**Distinguishing feature:** Lists primary-source-verified vs. not, and any gaps the parent should spot-check.

## Grading scorecard — honesty artifact

**Role:** Show the user whether the bundle actually meets the quality bar, with honest retrospective of earlier passes.

**Used when:** Same as QC report — parent review.

**Format constraint:** Every pass's grades appear in writing. When a later pass finds a gap, the earlier pass's grade is explicitly retrospectively downgraded — not silently re-issued.

**Distinguishing feature:** This is the anti-inflation discipline. It's what prevents the "all A's" trap that produces plausible-looking but incomplete study materials.
