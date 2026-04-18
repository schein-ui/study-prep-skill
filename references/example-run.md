# Pilot Run: 9th-Grade Evolution (April 2026)

Brief summary of the run this skill was extracted from. Use this as a reality check: "did my current run follow this pattern?"

## Setup

- **Student:** Chloe, 9th grade, Columbia Grammar
- **Subject:** Biology Unit 8 — Evolution
- **Test date:** Tue 2026-04-21
- **Run start:** Sat 2026-04-18 (3 days to test)
- **Materials provided:** teacher slide decks (Evolution 25-26.pptx.pdf, 37 slides; Evolution of Populations.pptx.pdf, 34 slides), Chloe's completed Ch 17 + Ch 18 reading guides (PDFs of typed answers)
- **Handoff doc provided:** yes — listed 6 claimed errors in Chloe's work, locked T1-T8 execution plan, user said Hardy-Weinberg explicitly excluded

## What went right

- **Complete deliverable set produced:** glossary · standalone HTML study guide · quiz bank · 2-page cheat sheet · 3-day study plan · Quizlet export · 8 SVGs · QC report · grading scorecard.
- **Hardy-Weinberg excluded everywhere** (verified via grep — only appears as exclusion notices).
- **Multi-format delivery:** iCloud Drive sync + Apple Mail draft + local folder.
- **All student-facing files openable without a build step.**

## What went wrong — and why the skill codifies guardrails

### 1. v1 graded against handoff summary, not primary source

The handoff listed 6 errors. I verified all 6 appeared in deliverables, declared Accuracy = A, and moved on. User supplied the reading-guide PDFs mid-run. Direct verification of Chloe's actual answers surfaced a **7th error** — "phylogenetic" written for "polygenic" on Ch 18.1 Q4. This is a HIGH-severity word-mixup almost certainly intended as a test distractor.

**Skill guardrail:** `phases/audit.md` mandates line-by-line read of every student answer, not trust-the-summary. `phases/qc-and-grading.md` forbids above-B+ on Accuracy if you've only verified against a secondary source.

### 2. v2 stopped at text extraction of slides

First PDF tool (`pdftoppm`) failed. I declared slides "unverifiable" and proceeded. PyMuPDF was installed the whole time. User had to prompt me to try a second tool.

**Skill guardrail:** `phases/primary-source.md` §"Anti-pattern: giving up after one failure" — and mandates documenting tool failures before claiming unverifiability.

### 3. v3 extracted slide text but not slide images

Text extraction of 71 slides gave me prose and some embedded table text. But the critical test-adjacent content was images: the "Build a Cladogram" character table (slide 34), the Tetrapoda cladogram example (slide 32), Human vs Ostrich classification (slide 29), hemoglobin amino-acid sequences (slide 37), teacher-specific selection examples (cactus spines for directional/stabilizing, butterflies for disruptive — slides 14-16).

User flagged: "how can you review the images that don't have text?"

**Skill guardrail:** `phases/primary-source.md` requires **Level 3 (image rendering)** for completeness. Level 2 alone is insufficient.

### 4. v1/v2/v3 grade inflation was not honestly retrospectively acknowledged

After each pass, I issued new grades without explicitly downgrading earlier passes that had been based on incomplete verification. User instructed: "ensure no grade inflation."

**Skill guardrail:** `phases/qc-and-grading.md` requires retrospective downgrades in writing. `SKILL.md` §"Honest Grading Retrospective Protocol" specifies the scorecard structure.

### 5. Initial deliverable was `.jsx` — student couldn't open it

The study guide was a React single-file component. The student has no React dev environment. User: "I need this to all be downloadable for a teenager — should be pdfs or executables so that she can look at it easily."

**Skill guardrail:** `phases/deliverables.md` §"Standalone HTML study guide" forbids framework artifacts. The main artifact must be a standalone HTML that works on `file://` with no build.

### 6. Even standalone HTML didn't work on iPhone from iCloud

Student's primary device is an iPhone. iOS Files app doesn't render HTML in-app — it shows a broken preview. The student would have had to tap-share-open-in-Safari, which a 9th-grader won't figure out unprompted. User: "I can't get the html link to work."

**Resolution:** pushed to a public GitHub repo, enabled Pages, gave the student a real URL. One tap from any device, renders instantly.

**Skill guardrail:** `SKILL.md` §"Distribution" elevates GitHub Pages publishing to the PRIMARY distribution channel when `gh` CLI is available. iCloud/email are secondary. The skill's completion checklist now requires live-URL parity verification (md5 match between local HTML and curl-of-URL) before declaring the run complete.

## Final state

4 grading passes. Honest floor: A-. Bundle:
- 21 files in `chloe_downloads/` (HTML · 7 PDFs · 3 .docx · 8 diagram PDFs · Quizlet · README)
- Synced to iCloud Drive
- Apple Mail draft queued with zip attachment
- Process artifacts (QC report + grading scorecard) available for parent review

## Lessons that became skill guardrails

| Lesson | Codified in |
|--------|-------------|
| Handoff summaries are incomplete | `phases/audit.md` §1 |
| One tool failing ≠ unverifiable | `phases/primary-source.md` Escalation Ladder |
| Text extraction misses images | `phases/primary-source.md` Level 3 mandate |
| Silent grade re-issue is inflation | `phases/qc-and-grading.md` Retrospective Protocol |
| `.jsx` is unreadable to a teenager | `phases/deliverables.md` §"Standalone HTML" |
| Standalone HTML doesn't render from iOS Files app — needs real URL | `SKILL.md` §"Distribution" + `phases/qc-and-grading.md` §"Distribution QC" |
| "All A's on Pass 1" is a warning sign | `phases/qc-and-grading.md` Common Inflation Patterns |

## How to use this document

Before running the skill, skim this file. It's 5 minutes. It will save you from repeating these misses.

After running the skill, add your own lessons to `feedback_*.md` in the user's memory system — especially if you found a new failure mode the skill doesn't guard against.
