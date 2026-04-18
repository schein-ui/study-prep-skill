# Phase 4: Deliverable Production

## Goal

Produce the tiered bundle in formats the student can actually use. Every deliverable has a distinct pedagogical role (see `references/deliverable-roles.md`). Every artifact must be openable by the student without a build step.

## The mandatory bundle

Generate each of these. Skip none.

| File | Format | Notes |
|------|--------|-------|
| `glossary.md` + `.pdf` + `.docx` | Canonical terms | Source of truth, referenced by all other deliverables |
| `study_guide.html` | Standalone interactive | Main artifact; inlines all SVGs |
| `study_guide.pdf` | Print version | Same content, no interactivity |
| `quiz_bank.md` + `.pdf` + `.docx` | Practice quiz | 15-20 MC, 6-10 SA, 2-4 diagram, 2-3 FRQ |
| `cheat_sheet.html` + `.pdf` | 2-page visual-dense | Test-morning scan only |
| `study_plan.md` + `.pdf` + `.docx` | Day-by-day schedule | To the test date |
| `flashcards.txt` | Quizlet import | Tab-separated, Must-Know → Should-Know order |
| `visuals/*.svg` | Subject diagrams | 5-10 SVGs, embedded in HTML |
| `visuals/*.pdf` | Individual diagram PDFs | So student can pull up one at a time on phone |

## Standalone HTML study guide (the main artifact)

This is the deliverable the student will actually open. It must:

- Be a **single .html file** with all CSS and JS inlined
- Embed every SVG inline (no external `<img>` references)
- Work **offline** on any browser, phone, tablet, or desktop
- Render immediately when opened via `file://` (no server required)
- Use **plain HTML + vanilla JS**. No React, no Vue, no Tailwind, no build step.
- Have a **sidebar nav** with an "⚠ Errors in My Notes" tab that's visually urgent (red background, top of list)
- Include a **click-to-reveal quiz** for formative self-test

Scaffold: `templates/study_guide.html`. Replace all `TODO:` markers with subject-specific content.

### Why standalone HTML and not .jsx

The student is a 13-17 year-old. They do not have a React dev environment. A `.jsx` file is a text file to them.

`.html` is:
- Double-clickable on any OS
- Synced via iCloud / Dropbox / AirDrop without conversion
- Email-attachable
- Viewable on an iPhone via Files → Open in browser

This is not a style preference. `.jsx` artifacts are **broken artifacts** for this audience.

## Cheat sheet — exactly 2 pages

Print-PDF via Chrome headless. Page 1 = first half of unit; Page 2 = second half + error-watch callout.

Use a CSS grid (2 columns) with color-coded boxes per subtopic. Include:
- Key formulas / mnemonics / named mechanisms
- Comparison tables
- 1 visual summary if space allows
- The "⚠ Errors in My Notes" mini-callout (1-line reminder per error)

Scaffold: `templates/cheat_sheet.html`. Verify it fits on 2 pages by opening the output PDF.

## Quiz bank conventions

- MC: 4 options. **At least one option is a distractor built from the student's actual errors.**
- SA: include a "scoring target" paragraph showing what a full-credit answer contains
- Diagram: reference a specific diagram by name (matches a visual in the bundle)
- FRQ: include rubric-style scoring targets (e.g., "4-point response: (a) ..., (b) ..., (c) ..., (d) ...")

Scaffold: `templates/quiz_bank.md`.

## Study plan conventions

Day-by-day, from today to the test date. Each day has:
- **Time budget** (total hours, ~90-150 min for a middle/high-schooler)
- **Specific activities with minute estimates**
- **Rules** (retrieval > rereading, interleaving, no cramming past 9pm)
- **The day-before-the-test morning script** (cheat sheet scan only, 15 min max, then stop)

Scaffold: `templates/study_plan.md`.

## Flashcards

Tab-separated format, two sections (`=== MUST KNOW ===` and `=== SHOULD KNOW ===`). Each line: `Term<TAB>Definition`. No markdown; Quizlet import is plain text.

Order: highest-yield cards first. Scaffold: `templates/quizlet.txt`.

### Quizlet import — manual, but trivial thanks to Quizlet's AI-assisted import

Quizlet's import auto-detects tab/comma/newline separators and surfaces a preview before the student commits. Five steps total, not ten:

1. quizlet.com/create-set → log in.
2. Click "+ Import".
3. Paste the `.txt` contents.
4. Preview → save.
5. Use Learn mode on the appropriate study day.

Failure-mode note to include in the student README: if the preview looks like "one giant card" or everything smushed, manually toggle the separator settings to "Tab" and "New line." Usually not needed.

**Principle:** when a destination is AI-assisted (Quizlet, Notion, ChatGPT-based tools), don't over-engineer the handoff instructions. The tool handles most edge cases; a 5-step recipe with a failure-mode note is better than a 10-step prescriptive recipe. Over-specification reads as condescending AND creates more failure modes when the AI-assisted UI doesn't match the written steps exactly.

### When to skip Quizlet entirely

If the student already uses Anki, write an Anki deck instead (see `phases/deliverables.md` §Alternative-flashcard-formats). But don't do both — flashcard surfaces compete for the student's study time.

## SVG visuals

Write each visual to `visuals/<name>.svg`. Requirements:
- `viewBox` attribute (for responsive scaling)
- Text is actual `<text>` elements, not converted to paths (so it's copyable/readable by screen readers)
- Label every axis, every region, every species/object
- Color palette is clear and accessible (avoid red-green only for colorblind students)
- Include a short legend or callout box if the diagram isn't self-explanatory

For subjects with specific teacher examples (e.g., a specific cladogram, a specific graph on a specific slide), **reproduce the teacher's exact version**. Not a generic textbook version. The teacher's specific figure is what will appear on the test.

## Generation script pattern

Write a Python script that batch-produces PDFs + .docx:

```python
# Chrome headless for HTML → PDF
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
def html_to_pdf(html_path, pdf_path):
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer",
                    "--virtual-time-budget=2000",  # let JS execute
                    f"--print-to-pdf={pdf_path}",
                    f"file://{html_path}"], check=True, capture_output=True)

# Markdown → styled HTML → PDF (via Chrome)
import markdown
def md_to_pdf(md_path, pdf_path, title):
    html_body = markdown.markdown(Path(md_path).read_text(), extensions=["tables"])
    # Wrap in styled shell, write to temp, call html_to_pdf, delete temp

# Markdown → .docx (python-docx)
import docx
def md_to_docx(md_path, docx_path, title):
    # Parse headings / lists / tables / paragraphs from markdown
    # Apply docx styles (Heading 1, Heading 2, List Bullet, Light Grid for tables)
    # Save
```

Common gotcha: **Chrome headless doesn't wait for JS fetches.** If the HTML uses `fetch()` to load content, pre-render that content into static HTML before calling Chrome. `--virtual-time-budget=2000` helps but isn't bulletproof.

## Output structure

```
{output}/
├── (markdown sources)
├── visuals/
│   └── *.svg
├── student_downloads/           ← hand THIS folder to the student. Study material ONLY.
│   ├── README_for_<student>.txt ← lead with the live URL; explain the Quizlet import
│   ├── 00_START_HERE.html       ← standalone study guide with SVGs inlined
│   ├── <Student>_Study_Guide.pdf
│   ├── <Student>_Cheat_Sheet.pdf
│   ├── <Student>_Quiz_Bank.pdf
│   ├── <Student>_Study_Plan.pdf
│   ├── <Student>_Glossary.pdf
│   ├── <Student>_Glossary.docx
│   ├── <Student>_Quiz_Bank.docx
│   ├── <Student>_Study_Plan.docx
│   ├── <Student>_Flashcards.txt
│   └── diagrams_pdf/
│       └── *.pdf
└── for_parent/                  ← parent/tutor review only. DO NOT mix into student_downloads.
    ├── QC_Report.pdf
    └── Grading_Scorecard.pdf
```

**Never zip the run root.** Zip `student_downloads/` only for email/iCloud distribution. The student sees study material, not the grading of the study material.

## Checklist before QC

```
[ ] All 7 deliverable categories produced
[ ] Standalone HTML opens and renders offline — verified
[ ] Every SVG is inlined in the HTML (no external references)
[ ] Cheat sheet fits on exactly 2 pages — verified by opening the PDF
[ ] Every HIGH error from audit has at least one quiz distractor built from it
[ ] Every deliverable uses the correct answers in body content (silent correction)
[ ] README_for_<student>.txt written, names the double-click file
[ ] student_downloads/ folder is self-contained (everything student needs is there)
```
