# study-prep — Example Invocations

The skill is subject-agnostic. These three invocations — bio, history, math — illustrate the range.

## Example 1 — 9th-grade biology (the pilot)

**User says:** "My kid Chloe has an evolution test Tuesday. Here are the teacher's slides, her completed reading guides, and a note about what's excluded."

**What study-prep does:**
1. Unzips the materials. Catalogs 2 slide decks (71 pages) + 2 reading guides.
2. Confirms scope: "Ch 17, 18.1/2/3, 19 intro. Hardy-Weinberg excluded. Test = MC + SA + diagram."
3. **Extracts teacher slides** — text via PyMuPDF, **images via `get_pixmap`**. Surfaces teacher-specific figures: a Build-a-Cladogram character table, a Tetrapoda cladogram example, cactus/peccary examples for selection types.
4. **Audits Chloe's reading guides** — finds 7 HIGH errors + 1 spelling. Each becomes a quiz distractor.
5. Produces: glossary · standalone HTML study guide with 8 inline SVGs · 16-question interactive quiz · 2-page cheat-sheet PDF · 3-day plan · Quizlet `.txt` · PDFs of all markdown · `.docx` of key files for Google Docs upload.
6. QC + 4 grading passes with honest retrospective on each.
7. Syncs bundle to iCloud Drive; opens Apple Mail composer with zip attached.

## Example 2 — High-school AP US History

**User says:** "My son Jake has an AP US History test Friday on Reconstruction through Gilded Age. Here's the teacher's review packet and his last three essays."

**What study-prep does:**
1. Catalogs 1 review packet (47 pages) + 3 essays.
2. Confirms scope: "Reconstruction 1865-1877; Gilded Age 1877-1898; robber barons, labor movement, populism, imperialism pivot. Test = DBQ (25 pts) + LEQ (15 pts) + multiple MC."
3. **Extracts** review packet text + renders images (timeline diagrams, political cartoons are always image-based).
4. **Audits essays** — finds recurring thesis weaknesses (Jake doesn't contextualize), factual errors (mixed up Credit Mobilier and Whiskey Ring), and one misattributed quote.
5. Produces:
   - **Glossary** — 40 terms (Reconstruction Amendments, Bessemer process, Pullman Strike, Jim Crow, Dawes Act, etc.), with trap-list for similar-sounding names Jake mixed up.
   - **Standalone HTML study guide** — 5 sections, embedded timeline SVGs, interactive DBQ/LEQ builders.
   - **Quiz bank** — MC items using Jake's actual name-confusions as distractors; DBQ + LEQ prompts with rubric scoring targets.
   - **Cheat sheet** — 2 pages: Amendment comparison table, key-figures table, timeline, thesis template.
   - **Study plan** — 3 days: comprehension · practice DBQ under time · LEQ + cheat sheet scan.
   - **Flashcards** — 60 cards, term-definition + cause-effect format.
6. Same QC + grading + distribution.

## Example 3 — Middle-school pre-algebra

**User says:** "Ava has a pre-algebra test on linear equations and systems Wednesday. Her teacher posted a practice test and she did 6 problems for homework."

**What study-prep does:**
1. Catalogs practice test (10 pages) + homework (6 problems).
2. Confirms scope: "Solving 2-step equations; graphing linear equations; systems by substitution and elimination; word problems."
3. **Extracts** practice test. Even for math, image rendering matters: graph problems are image-based, and the teacher's specific coordinate-axis styling (if idiosyncratic) matters.
4. **Audits homework** — Ava gets slope-intercept form right but consistently confuses positive and negative slopes when reading a graph; she also drops the negative sign when distributing -3 into a parenthesis.
5. Produces:
   - **Glossary** — slope, y-intercept, point-slope form, standard form, system of equations, substitution, elimination, consistent/inconsistent/dependent systems.
   - **Standalone HTML study guide** — worked examples for each problem type, SVG of slope +/-/0/undefined reference chart.
   - **Quiz bank** — items explicitly built around Ava's two specific errors (negative-slope reading, distribution sign-drop).
   - **Cheat sheet** — 2 pages: slope reference chart, solving-2-step-equation steps, substitution-vs-elimination decision tree, word-problem setup template.
   - **Study plan** — 2 days before + test morning.
   - **Flashcards** — formulas + error-correction pairs (Ava-wrote vs. correct).
6. Same QC + grading + distribution.

## What stays constant across subjects

- **Primary-source escalation to Level 3** (text + images) — mandatory
- **Audit the student's own work** — mandatory; errors become quiz distractors
- **Tiered deliverable set** — all 7 deliverables, every time
- **Formats the student can open** — standalone HTML + PDFs + .docx + flashcards + diagram PDFs
- **Anti-inflation grading** — honest retrospective on every pass

## What varies by subject

- **Domain expert casting** — Patel (molecular biologist) for bio, a historian for AP US History, a math teacher + problem-solving specialist for math.
- **Visuals** — what's visual varies. Bio: cladograms, homology diagrams. History: timelines, cartoons, maps. Math: graphs, geometric diagrams.
- **Quiz format weights** — FRQ-heavy for AP History, word-problem-heavy for math, diagram-heavy for bio/anatomy.
- **Study-plan rhythm** — bio and history benefit from interleaving across chapters. Math is more sequential; don't force interleaving that breaks logical build-up.
