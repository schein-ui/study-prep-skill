---
name: study-prep
description: Produce a complete, student-usable test-prep bundle from teacher materials + the student's own completed work. Subject-agnostic. Audits the student's work against the primary source, surfaces their specific errors as "Watch Out!" cards, and produces PDFs + a standalone interactive HTML + Google Docs + flashcards + visuals. Composes with agentloop for the multi-expert review and grading loop.
---

# study-prep

## What this skill does

A parent/tutor hands you (a) teacher-distributed materials (slides, reading guides, worksheets), (b) the student's own completed homework or notes, and (c) a test date + format. You produce a tiered study bundle the student can actually use on their phone, iPad, or laptop — **not just markdown files**.

This skill is subject-agnostic. It's been piloted on a 9th-grade evolution test; the logic works equally well for math, history, foreign language, literature, AP science, etc.

## When to invoke

Use when the user:
- Asks for a study guide / test prep / review packet for a specific upcoming test
- Provides their child's or student's completed work alongside teacher materials
- Says "my kid has a test on [date], help them study"
- References a specific class unit, chapter, or exam

Do NOT invoke for:
- Generic "explain X concept" requests (use teaching/explanation skills)
- College-level research writing (different toolset)
- One-off flashcards with no surrounding test context

## Core principles (non-negotiable)

1. **Audit the student's own completed work** against the primary source. This is the single highest-leverage move. Every wrong answer the student has lived with becomes a "Watch Out!" correction in the bundle. Don't skip this because "the teacher graded it" — teachers often grade for completion.

2. **Primary-source escalation is mandatory.** Summary → text extraction → image rendering. If one PDF tool fails, try another before declaring unverifiable. Slide/textbook figures frequently carry the specific example the teacher will test on.

3. **Grade honestly with an anti-inflation retrospective.** If a later pass finds a gap, retrospectively downgrade the affected earlier-pass grades in writing. Never quietly re-issue as the same grade.

4. **Deliver in formats the student actually uses.** No React/JSX artifacts the student can't run. Deliver: PDFs, standalone HTML, Google Docs (.docx), flashcards (.txt), and individual diagram PDFs. Sync to iCloud or email — don't leave files in a dev directory.

5. **Compose with agentloop.** This skill is the domain scaffolding. Use `agentloop` at `~/.claude/skills/agentloop/` for the team/debate/grading machinery. Don't duplicate roundtable, casting, or grading protocols — invoke them.

## Inputs you collect

| Input | What it is | Source |
|-------|-----------|--------|
| **Teacher materials** | slides (PPTX/PDF), reading guides, worksheets, syllabus, previous test reviews | Parent provides path or files |
| **Student work** | student's completed reading guides, prior homework, class notes, prior quizzes | Parent provides |
| **Test date** | absolute date; convert "Tuesday" → ISO date | Ask if unclear |
| **Test format** | MC/SA/FRQ/diagram/essay mix; any explicit exclusions (e.g., "skip chapter X") | Ask if unclear |
| **Grade/level** | 6th grade, high school, AP, college — controls language level | Infer or ask |
| **Student profile** | strengths, learning-style signals (visual/kinesthetic/ADHD/ESL), specific anxieties | Optional but useful |

If the user provides a pre-written handoff document (like a prompt.txt describing the run), read it first — it may contain constraints, locked decisions, or errors to address that shouldn't be re-derived.

## Phase structure

Each phase has a companion file in `phases/` — **Read the phase file before entering it.** Full procedural detail lives there; this file is the map.

| Phase | File | Output |
|-------|------|--------|
| 1. Intake | `phases/intake.md` | Run directory, materials catalog, scope statement |
| 2. Primary-source extraction | `phases/primary-source.md` | All teacher content accessible (text + images), images rendered |
| 3. Student-work audit | `phases/audit.md` | List of HIGH/MEDIUM/LOW severity errors in student's work, with source location |
| 4. Deliverable production | `phases/deliverables.md` | Tiered bundle: glossary + interactive HTML + quiz + cheat sheet + plan + flashcards + visuals |
| 5. QC + grading loop | `phases/qc-and-grading.md` | Passes graded with anti-inflation retrospective |
| 6. Distribution | (this file §Distribution below) | Bundle sync'd to iCloud / emailed / Google Docs |

## Mandatory Primary-Source Escalation Protocol

This is the protocol that kept catching misses in the pilot run. Don't shortcut.

```
ESCALATION LADDER — keep going until primary source is fully verified

Level 1: Summary only (handoff doc, prior session, what the user said)
  → Insufficient. Every pilot run's Level-1 "complete" proved incomplete.

Level 2: Text extraction from primary PDFs/docs
  Tools to try, in order: pdftotext → PyMuPDF (`import fitz`) → pdfplumber → pypdf
  If all fail, report to user and ask for an alternative file format.

Level 3: Image rendering of PDFs
  Text extraction misses tables-as-images, diagrams, figures, hand-drawn charts,
  and slide graphics. Render each page as PNG, view with image-reading tool.
  Tools: PyMuPDF get_pixmap, sips, qlmanage.

Level 4: Student-work audit
  Apply the escalation to the student's own work too. Surface each error
  with exact citation (which page, which question).
```

Anti-pattern: "this PDF tool failed so I'm treating the slides as unverifiable." One tool failing is not the end. Try another. If ALL fail, tell the user explicitly and ask.

## Mandatory Student-Work Audit Protocol

The single most valuable move in this skill. The student has been studying with WRONG answers since they submitted the homework — fix that before anything else.

```
AUDIT PROTOCOL

1. Line-by-line: read each question + student's answer against the primary source.
2. For each answer, classify: CORRECT / HIGH-severity wrong / MEDIUM / LOW (spelling) / INCOMPLETE.
3. For each HIGH/MEDIUM, note: (a) exact location (Ch/page/question), (b) what student wrote,
   (c) correct answer, (d) why the error matters — what concept is actually being missed.
4. In every deliverable:
   - USE the correct answer in body content (silent correction)
   - SURFACE the error in a dedicated "Errors in My Notes" section with the wrong/correct pair
5. Order the errors section FIRST in the student's study path. Research (refutation text):
   seeing the wrong version and the correct version side-by-side overwrites more reliably
   than seeing only the correct version.
```

Common error types to watch for (from pilot runs):
- Typos the student didn't catch (e.g., "cavitation" instead of "variation")
- Copy-paste errors between questions
- Word-mixups from near-homophones (e.g., "polygenic" vs. "phylogenetic")
- Circular definitions ("X is what happens when X happens")
- Factual errors the teacher didn't correct (completion grading)
- Missing answers / blank questions

## Deliverable set (mandatory)

Every run produces this tiered bundle. Each deliverable has a distinct pedagogical role. See `references/deliverable-roles.md` for the research rationale.

| Deliverable | Format | Pedagogical role | Used when |
|-------------|--------|-----------------|-----------|
| **Glossary** | Markdown + PDF + .docx | Source of truth for terms | Reference; not primary study material |
| **Interactive study guide** | **Standalone HTML** (no build step, no framework) | Primary reading | Day 1: comprehension |
| **Quiz bank** | Markdown + PDF + .docx | Active recall | Day 2: spaced retrieval |
| **Cheat sheet** | HTML → 2-page PDF | Visual-dense scan | Test morning: 15-min scan only |
| **Study plan** | Markdown + PDF + .docx | Day-by-day schedule | Day 0: set the pace |
| **Flashcards** | Tab-separated .txt (Quizlet import) | Spaced repetition | Any day, phone/commute |
| **Consolidated PRINT PACK** | Single PDF, ≤25 pages | One artifact to print + carry; staple-ready | Day 1 print → use through test |
| **SVG visuals** | Inline in HTML + individual PDFs | Visual reinforcement | Throughout |
| **QC report + grading scorecard** | Markdown + PDF | Process artifacts for the parent | Parent review |

### Consolidated print pack — required, ≤ 25 pages

Single PDF combining: cover + TOC + study plan + glossary + study guide content + cheat sheet + quiz bank with answers. The student prints ONE document, staples it, carries it to the kitchen table. No flipping between tabs, no opening 5 PDFs.

**Target structure (page budget — adjust within the 25-page cap):**
- Cover (1)
- TOC + "how to use this pack" (1)
- Study plan (1–2)
- Glossary (3–5)
- Study guide content (8–12)
- Cheat sheet (2)
- Quiz bank with answers inline (4–6)

**File:** `<Student>_<Subject>_Complete.pdf` in the student_downloads/ folder.

### Hard cap: full study guide ≤ 25 pages

This applies to **every full-content artifact** — the consolidated print pack, the study-guide PDF, and any other "full content" output. The cheat sheet stays at 2 pages; the quiz bank can be longer if needed (separate file). But the comprehensive document itself never exceeds 25 pages.

**Why:** a 50-page study packet is a wall, not a tool. A 25-page packet is a 1-hour read or a 30-minute review. Compression forces clarity — if a section feels bloated, cut.

**How to enforce when generating:**
1. Use 10–10.5pt body text, 22pt H1, 13pt H2 — not "look like a textbook" 12pt+.
2. Keep tables compact (9.5pt cell text, 3pt padding).
3. Embedded SVGs sized to fit in ½–⅔ of a page — not full page each.
4. Any retrieval/check-yourself blocks are tight 5–6 line callouts, not full pages.
5. **Verify after generation:** `python3 -c "import fitz; print(len(fitz.open('path.pdf')))"` — if > 25, trim.
6. If the natural content really needs more than 25 pages, split into the consolidated pack PLUS a separate "Reference / Glossary" PDF — but the consolidated pack itself must stay ≤ 25.

**Common over-runs and what to cut:**
- Repeated explanations across glossary + study guide → keep in one place, reference from the other
- 3-line bulletpoints when a one-line dash list would do
- Multiple "Watch Out" callouts with the same takeaway — consolidate to one
- Quiz "scoring target" answers > 6 lines each — trim to 3
- Unused sections (e.g., "Test traps" duplicating the errors-from-notes block)

**Critical delivery format requirements:**
- **The interactive guide is STANDALONE HTML.** No React, no JSX, no Tailwind, no build step. Plain HTML + CSS + vanilla JS. All SVGs inlined. Works offline, works on phone, works on any browser. The student double-clicks it.
- **The cheat sheet is a real PDF.** Generated via Chrome headless from HTML.
- **Markdown-based deliverables get both PDF (via Chrome headless) AND .docx (via python-docx) versions.** Markdown alone is not student-usable.
- **No artifacts the student can't open.** If you can't point at a file and say "double-click this," it doesn't count.

See `phases/deliverables.md` for templates and the generation script pattern.

## Composition with agentloop

This skill does not re-implement agentloop. It invokes it at specific points:

| Study-prep moment | agentloop phase used |
|-------------------|----------------------|
| Casting: assemble domain experts (subject teacher + learning scientist + assessment specialist + skeptic) | Phase 1 Scoping |
| Roundtable debate on approach, prioritization, what to exclude | Phase 2 Roundtable |
| Production of deliverables with multi-expert review | Phase 3 Execution |
| Grading loop with 6 criteria (Content Accuracy · Curriculum Fit · Pedagogy · Assessment Quality · Engagement · Cross-Deliverable Consistency) | Phase 4 Grading |

The study-prep skill adds: the student-work audit, the primary-source escalation protocol, and the deliverable-format discipline. It does not replace agentloop's machinery.

Typical team (Casting Director selects):
- **Subject teacher** (domain expertise, grade-level fit)
- **Domain specialist** (accuracy, e.g. molecular biologist for bio, math Ph.D. for math)
- **Learning scientist** (pedagogy, retrieval practice, refutation text)
- **Assessment specialist** (quiz construction, distractor design)
- **Skeptic / error hunter** (QC, verifies primary-source audit was complete)

## Honest Grading Retrospective Protocol

When a later pass surfaces a gap, retroactively acknowledge that the earlier pass's grade was inflated. Do NOT silently re-issue the same grade number.

```
GRADING SCORECARD STRUCTURE

For each pass N:
  Section 1: Pass N grades (what the graders assigned with evidence)
  Section 2: IF a later pass finds a primary-source gap that affects Pass N criteria:
             show Pass N grade | honest Pass N grade | reason | criteria affected
  Section 3: What changed between Pass N and Pass N+1
```

Pilot-run example (in `references/example-run.md`):
- Pass 1 Accuracy = A based on handoff summary. Later found: reading guides contained error #7 that the summary didn't list.
- Retrospective: Pass 1 Accuracy should have been B+, not A.
- Pass 2 (post-fix) Accuracy = A honestly.

This discipline was imposed by user instruction — and it surfaced 3 separate rounds of misses in the pilot run.

## Distribution

The bundle is only useful if the student can open it. **Always do #1 (live URL) if `gh` is available** — it's the one format that works on an iPhone with a single tap. Complete at least one of the others too, for redundancy.

### 1. Live URL via GitHub Pages (STRONGLY RECOMMENDED — iPhone-compatible)

iCloud Drive HTML files won't render in iOS Files app. Emailed .html attachments get blocked by Gmail. The only reliable "student taps one link on her phone and it works" path is a real URL.

**Procedure:**

```bash
# Prereqs: gh CLI installed + authenticated. Check:
gh auth status

# 1. Check GitHub plan — private Pages needs Pro/Team; free plan = public only
gh api user --jq '.plan.name'

# 2. If user is on free plan AND content contains PII (student name, specific homework
#    citations), ask whether to make public OR pseudonymize first. Don't silently publish.

# 3. Create repo + push
TMP=$(mktemp -d) && cd "$TMP"
cp "<output>/student_downloads/00_START_HERE.html" index.html
git init -q -b main
git add index.html
git -c user.name="$(gh api user --jq .login)" \
    -c user.email="$(gh api user --jq '.email // "noreply@github.com"')" \
    commit -q -m "<student> <subject> study guide"

REPO="<username>/<student>-<subject>"   # e.g., schein-ui/chloe-evolution
gh repo create "$REPO" --public --description "<subject> study guide for <student>"
git remote add origin "https://github.com/$REPO.git"
git push -u origin main

# 4. Enable Pages
gh api --method POST /repos/$REPO/pages \
  -f 'source[branch]=main' -f 'source[path]=/'

# 5. Poll URL until live (typically ~60s)
URL="https://$(echo $REPO | cut -d/ -f1).github.io/$(echo $REPO | cut -d/ -f2)/"
until [ "$(curl -s -o /dev/null -w '%{http_code}' $URL)" = "200" ]; do sleep 15; done
echo "LIVE: $URL"
```

**What gets pushed:** only the standalone HTML (as `index.html` so it serves at the repo root). NOT the PDFs (too much bulk; parent emails those separately), NOT the student's completed work (privacy), NOT the state/QC files (process artifacts).

**PII discipline:** Before pushing to a public repo, decide:
- Is the student's name in the HTML? (yes, by default)
- Are there citations to the student's specific homework pages? (yes, in error cards)
- Is the content otherwise identifiable?

If the user is OK with public content as-is, publish. If not, offer to pseudonymize ("Chloe" → "Student", specific citations → generic "Ch X Qn"). Ask explicitly.

**Update workflow:** if the content changes after publishing, `cd` into the repo clone and `git push` — updates propagate in ~60 seconds. Encourage this over creating new repos.

### 2. iCloud Drive (for Apple-device users)

Copy `student_downloads/` folder to `~/Library/Mobile Documents/com~apple~CloudDocs/<student>'s <subject> Kit/`. Syncs to all Apple devices. Useful as a **secondary** distribution — PDFs open fine in iOS Files, .docx files open in iOS Pages or Google Docs, but the HTML will only render if the student Shares → Opens in Safari (annoying UX — the live URL is better).

### 3. Email via Apple Mail

Zip the bundle, use AppleScript to compose a message with the zip attached + parent's address pre-filled. Parent reviews and clicks Send. Useful for: parents who don't use iCloud, off-Apple recipients, or as a paper-trail handoff. **Gmail may block the `.html` attachment inside the zip** — if so, the recipient has to unzip.

### 4. Google Drive / Dropbox (check availability)

```bash
ls ~/Dropbox ~/Library/CloudStorage/ 2>/dev/null
```

If either is mounted, copy there as a third backup. The parent uploads the `.docx` files manually to Google Drive if they want them as Google Docs.

### Distribution priority summary

| Student device | Do this |
|----------------|---------|
| iPhone / iPad | Live URL (GitHub Pages) — primary. iCloud — backup for PDFs. |
| Android / Windows laptop | Live URL + emailed zip |
| Mac | Any — the standalone HTML + double-click works directly |
| No internet at test time | Parent emails the zip; student extracts + opens `00_START_HERE.html` offline |

## Output directory convention

Mirror agentloop's conventions. **Critical:** process artifacts (QC report, grading scorecard) belong in a `for_parent/` folder, NEVER inside `student_downloads/`. The student should open their folder and see only study material — not the grading of that material.

```
{working_dir}/study-prep-output/{run-id}/
├── glossary.md                     ← markdown source
├── study_guide.html                ← standalone interactive (the main artifact)
├── quiz_bank.md
├── cheat_sheet.html                ← 2-page print HTML
├── study_plan.md
├── flashcards.txt
├── visuals/
│   └── *.svg                        ← 5-10 subject-specific diagrams
│
├── student_downloads/               ← the "hand this to the student" folder. STUDY MATERIAL ONLY.
│   ├── README_for_<student>.txt
│   ├── 00_START_HERE.html           ← standalone (SVGs inlined)
│   ├── <Student>_Study_Guide.pdf
│   ├── <Student>_Cheat_Sheet.pdf
│   ├── <Student>_Quiz_Bank.pdf
│   ├── <Student>_Study_Plan.pdf
│   ├── <Student>_Glossary.pdf
│   ├── <Student>_Glossary.docx      ← upload to Google Docs
│   ├── <Student>_Quiz_Bank.docx
│   ├── <Student>_Study_Plan.docx
│   ├── <Student>_Flashcards.txt     ← Quizlet import
│   └── diagrams_pdf/
│       └── *.pdf                     ← each visual as its own PDF
│
├── for_parent/                      ← process artifacts — parent/tutor review only
│   ├── QC_Report.pdf                 ← what was verified, what wasn't, any gaps
│   └── Grading_Scorecard.pdf         ← honest multi-pass grading with retrospective
│
├── qc_report.md                     ← markdown sources for parent artifacts
└── grading_scorecard.md
```

`{run-id}` format: `YYYY-MM-DD_<subject-slug>` (e.g., `2026-04-18_evolution`).

**Also critical:** when zipping + distributing, zip only `student_downloads/`, never the whole run directory. The parent folder stays local (or goes to a separate iCloud spot if the parent wants access on their phone).

## Templates

Under `templates/`:

- `glossary.md` — canonical-term list scaffolding
- `study_guide.html` — standalone HTML shell with sections nav, click-to-reveal quiz, callout/err/retrieval CSS classes
- `quiz_bank.md` — MC/SA/diagram/FRQ template with scoring-target format
- `cheat_sheet.html` — 2-page print CSS grid
- `study_plan.md` — day-by-day schedule structure
- `quizlet.txt` — tab-separated format with Must-Know / Should-Know sections

Each template has TODO markers where subject-specific content goes. Don't publish a template with TODOs unreplaced.

## Checklist before declaring a run complete

```
[ ] Primary-source escalation to Level 3 (images rendered and read) — not just text extraction
[ ] Student-work audit complete — every wrong answer surfaced + silently corrected
[ ] All deliverables exist in student-usable formats (PDF + standalone HTML + .docx where appropriate)
[ ] No .jsx / .md-only / framework-dependent artifacts in the student_downloads/ folder
[ ] Distribution PRIMARY: live URL via GitHub Pages published, HTTP 200, MD5 parity confirmed
[ ] Distribution SECONDARY: iCloud sync AND/OR email draft
[ ] Grading scorecard includes honest retrospective for every pass — no silent re-issues
[ ] README_for_<student>.txt tells them what to double-click first (and cites the live URL)
[ ] Cheat sheet fits on exactly 2 pages (verify via PDF)
[ ] Consolidated print pack PDF generated AND verified ≤ 25 pages (via fitz)
[ ] Full study guide PDF verified ≤ 25 pages (via fitz)
[ ] Standalone HTML opens offline and renders all SVGs inline (no external refs)
[ ] Live URL renders identical content to local HTML (md5 match)
```

Any unchecked box = run is not complete.

## Anti-patterns

- ❌ "Here's a React component you can drop into your app." The student can't run React.
- ❌ Grading everything A+ on first pass. Almost certainly inflated. At least one criterion is B range on Pass 1 — find which.
- ❌ Treating the teacher's handoff summary as complete. The summary is always incomplete. Verify primary.
- ❌ Stopping at text extraction. Images carry specific test content.
- ❌ Delivering only markdown. The student won't open markdown on their phone.
- ❌ Silent re-issuing of grades when later passes find gaps. Flag it.

## See also

- `EXAMPLES.md` — three sample invocations (math, history, bio) showing subject-agnosticism
- `references/pedagogy-notes.md` — why each deliverable exists (retrieval > rereading, refutation text, interleaving)
- `references/deliverable-roles.md` — what each deliverable format is for
- `references/example-run.md` — summary of the evolution pilot run
