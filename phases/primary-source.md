# Phase 2: Primary-Source Extraction

## Goal

Achieve **Level 3** verification (text + images) against all teacher materials. Not Level 1 (summary). Not just Level 2 (text extraction). The pilot run proved that each level surfaced distinct content; stopping early means shipping with gaps.

## The escalation ladder

```
Level 1: Handoff summary / prior session / user description
  → Always insufficient. Use only to plan; never to verify.

Level 2: Text extraction from PDFs, PPTX, DOCX
  → Gets the prose but misses diagrams, tables-as-images, hand-drawn figures,
    slide graphics, and anything rendered as an image rather than text.
    Typical misses in pilot: "Build a Cladogram" table, example diagrams,
    specific teacher examples (e.g., "bee wing and bat wing" when only "bee"
    is in the body text).

Level 3: Image rendering
  → Render every page as PNG, read as image. Catches everything Level 2 missed.
    Typically adds 5-15 domain-specific items per subject.

Level 4: Student work (separate protocol — see audit.md)
```

Never declare verification "done" before reaching Level 3.

## Tools — try in order, fall through on failure

### For text extraction (Level 2)

```python
# Preferred: PyMuPDF
import fitz
doc = fitz.open(path)
for page in doc:
    text = page.get_text()
```

Fallback order:
1. `pdftotext` (poppler) — CLI, widely available
2. `PyMuPDF` — usually pre-installed on macOS
3. `pdfplumber` — best for table extraction
4. `pypdf` — pure Python fallback

Command-line availability check:
```bash
which pdftotext mutool pdfinfo 2>&1
python3 -c "import fitz; print(fitz.__version__)" 2>&1
python3 -c "import pdfplumber; print('ok')" 2>&1
python3 -c "import pypdf; print(pypdf.__version__)" 2>&1
```

### For image rendering (Level 3)

```python
# PyMuPDF
import fitz
doc = fitz.open(path)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=110)
    pix.save(f"slide_{i+1:02d}.png")
```

macOS fallbacks:
- `sips` (built-in) — convert image formats
- `qlmanage` (built-in) — generate Quick Look previews
- Chrome headless: `--screenshot` flag

### Anti-pattern: giving up after one failure

Pilot run: `pdftoppm` wasn't installed, so I declared slides unverifiable and moved on. PyMuPDF's `get_pixmap` was installed the whole time. The user had to prompt me to try another tool.

**Rule:** when one tool fails, explicitly try the next tool in the fallback list. Only declare unverifiable after exhausting the list AND reporting to the user.

## Procedure

### 1. Run text extraction on every teacher material file

Write extracted text to `{state}/extracted/<filename>.txt`. Include page numbers as markers.

### 2. Read the extracted text

Skim for:
- Chapter/unit headings
- Defined terms (anchor these for the glossary)
- Teacher-specific examples ("cactus spines and peccaries," "Eastern vs. Western meadowlark")
- Mnemonics (memorize exact phrasing; teachers test the exact wording)
- Tables (values, rows, columns — these are often on tests verbatim)
- Explicit exclusion notes ("SKIP section X," "will not be on test")

### 3. Render every page as an image

Output to `{state}/rendered_images/<filename>_p<N>.png`.

### 4. View each rendered image

Prioritize image-heavy pages. Indicators that a page likely has test-critical imagery:
- Page labeled "Practice," "Exercise," "Build a..." — these are usually on the test
- Pages with tables visible in text extraction but incomplete data
- Any page whose extracted text is <50 words but the PDF page has content (= the content is an image)
- Slides with single-noun titles ("Classification," "Cytochrome C," "Cladograms") — usually have a figure

### 5. Note teacher-specific vs. generic examples

When the teacher uses a specific example, it goes on the test. Textbook-generic examples the teacher didn't mention are less likely to appear. Flag the distinction when populating deliverables:

```
Teacher's example (slide N): <specific>
Textbook example: <generic — optional fallback>
```

### 6. Produce an extracted-content summary

Write `{state}/primary_source_verified.md`:

```markdown
# Primary-Source Extraction — Level 3 Complete

## Text extraction
- <file1>: <N pages>, <source tool used>, text saved to <path>
- <file2>: ...

## Image rendering
- <file1>: <N PNGs in rendered_images/>
- <file2>: ...

## Teacher-specific content inventory
- Mnemonics: <list with exact phrasing>
- Specific examples: <list with slide numbers>
- Tables/figures on-the-test-for-sure: <list>
- Explicit exclusions: <list>

## Handoff items for Audit phase
- <anything that affects how student work is evaluated>

## Gaps (if any)
- <unextractable file + tool-failure trail — ONLY if all fallbacks failed>
```

## Checklist before proceeding to audit

```
[ ] Every teacher file has text extraction — written to disk
[ ] Every teacher file has image renders — saved to disk
[ ] Image-heavy pages have been viewed
[ ] Teacher-specific examples catalogued separately from textbook-generic ones
[ ] Exclusions captured
[ ] primary_source_verified.md written
[ ] Any "unverifiable" claim is backed by documented failures of ≥3 tools
```
