# study-prep

Claude Code skill that produces a complete, student-usable test-prep bundle from teacher materials + the student's own completed work.

Subject-agnostic. Built from a pilot run for a 9th-grade evolution biology test (see `references/example-run.md`); works equally well for math, history, literature, foreign language, AP sciences.

## What it does

Given:
- **Teacher materials** (slides, reading guides, worksheets, syllabus)
- **The student's own completed work** (homework, notes, prior quizzes)
- **A test date + format**

Produces a tiered bundle the student can actually use on their phone:
- Interactive standalone HTML study guide (no React, no build — just `index.html`)
- Published to GitHub Pages automatically, so the student taps a URL from any device
- 2-page print-ready cheat sheet (PDF)
- 30-item quiz bank with distractors built from the student's actual errors
- Day-by-day study plan
- Canonical glossary + Quizlet-importable flashcards
- Subject-specific SVG diagrams
- Google Docs–ready `.docx` versions of markdown deliverables

## Core principles (non-negotiable)

1. **Audit the student's own completed work** against the primary source. Errors become "Watch Out!" cards and quiz distractors. Research-backed refutation text.
2. **Primary-source escalation:** summary → text extraction → image rendering. Don't stop at text; images carry test-critical content.
3. **Honest iterative grading.** If a later pass finds a gap, retroactively downgrade earlier passes in writing. No silent re-issues.
4. **Deliver in formats the student actually uses.** No framework artifacts, no `.jsx`, no markdown-only. Live URL + PDFs + standalone HTML + Google Docs.
5. **Compose with [agentloop](https://github.com/anthropics/claude-code-skills) (or similar)** for the multi-expert team/debate/grading loop. Don't reimplement that machinery.

## Installation

```bash
git clone https://github.com/schein-ui/study-prep-skill.git ~/.claude/skills/study-prep
```

Or, if you prefer a different skill directory:

```bash
git clone https://github.com/schein-ui/study-prep-skill.git <your-claude-skills-dir>/study-prep
```

Claude Code picks up the skill automatically on next start. Trigger it by asking Claude to help prep for a specific test.

## Repo structure

```
study-prep/
├── SKILL.md                      # main skill file — Claude reads this first
├── EXAMPLES.md                   # three sample invocations (bio, history, math)
├── phases/
│   ├── intake.md                 # gather materials, confirm scope
│   ├── primary-source.md         # text + image extraction escalation
│   ├── audit.md                  # find errors in student's work
│   ├── deliverables.md           # produce the tiered bundle
│   └── qc-and-grading.md         # grading loop + distribution QC
├── templates/
│   ├── glossary.md
│   ├── study_guide.html          # standalone HTML scaffold
│   ├── quiz_bank.md
│   ├── cheat_sheet.html          # 2-page print-ready scaffold
│   ├── study_plan.md
│   ├── quizlet.txt
│   └── README_for_student.txt    # student-facing handoff note
└── references/
    ├── pedagogy-notes.md         # research citations for retrieval/refutation/interleaving
    ├── deliverable-roles.md      # what each deliverable is for
    └── example-run.md            # pilot run summary + lessons learned
```

## Requires

- Claude Code (any recent version)
- `gh` CLI authenticated (for GitHub Pages publishing — optional but strongly recommended)
- Python 3 + `PyMuPDF` (`pip install pymupdf`) for PDF text + image extraction
- `python-docx` (`pip install python-docx`) for .docx generation
- Chrome/Chromium (for HTML → PDF via headless rendering)

## Philosophy

**The student has been studying with wrong answers since they submitted the homework.** Teachers grade for completion; errors persist. The single highest-leverage move in test prep is a targeted audit of the student's own completed work, then surfacing those specific errors as refutation text (wrong version + correct version, side-by-side). Generic study guides miss this. This skill doesn't.

## License

MIT — use, modify, redistribute freely.

## Pilot run

See `references/example-run.md` for the evolution-biology run this skill was extracted from, including the four grading passes (each catching a different class of failure) that drove the mandatory protocols.
