#!/usr/bin/env python3
"""
Generate all PDF + DOCX outputs for Chloe's Biology Final study bundle.

Inputs:
  - study_guide.html
  - cheat_sheet.html
  - study_plan.md
  - glossary.md
  - quiz_bank.md
  - flashcards.txt
  - visuals/*.svg

Outputs (into student_downloads/):
  - 00_START_HERE.html              (study_guide with SVGs inlined)
  - Chloe_Study_Guide.pdf
  - Chloe_Cheat_Sheet.pdf
  - Chloe_Study_Plan.pdf
  - Chloe_Study_Plan.docx
  - Chloe_Glossary.pdf
  - Chloe_Glossary.docx
  - Chloe_Quiz_Bank.pdf
  - Chloe_Quiz_Bank.docx
  - Chloe_Flashcards.txt              (copy of flashcards.txt)
  - diagrams_pdf/*.pdf                (each SVG as a PDF)
  - Chloe_Biology_Complete.pdf         (consolidated print pack ≤ 25 pages)
"""
import os
import re
import shutil
import subprocess
from pathlib import Path
import fitz  # PyMuPDF
import markdown
from weasyprint import HTML, CSS
from docx import Document
from docx.shared import Pt, RGBColor, Inches

ROOT = Path(__file__).resolve().parent.parent
RUN = ROOT / "study-prep-output" / "2026-05-29_biology-final"
SD   = RUN / "student_downloads"
DIAG = SD / "diagrams_pdf"
VIS  = RUN / "visuals"

SD.mkdir(parents=True, exist_ok=True)
DIAG.mkdir(parents=True, exist_ok=True)

# ---------- 1. Standalone 00_START_HERE.html with SVGs inlined into ToC ----------
guide_html = (RUN / "study_guide.html").read_text()

# Build a "visuals" section listing each SVG inline at the end of each topic.
svg_inline = {}
for svg_path in sorted(VIS.glob("*.svg")):
    svg_inline[svg_path.stem] = svg_path.read_text()

# Inject visuals before relevant section closing tags.
mappings = [
    ("topic-2", "01_central_dogma"),       # Central Dogma → RNA section
    ("topic-3", "04_meiosis_phases"),      # Meiosis phases → Meiosis section
    ("topic-4", "06_punnett_squares"),     # Punnett squares → Genetics section
    ("topic-6", "05_energy_pyramid"),      # Energy pyramid → Ecology section
    ("topic-7", "02_heart_blood_flow"),    # Heart → Human Body section (intentionally first)
]
# also add respiratory at top of topic-7 (after heart)
for section_id, svg_stem in mappings:
    svg = svg_inline.get(svg_stem, "")
    if not svg:
        continue
    # Drop the <?xml?> line if present so it inlines cleanly into HTML
    svg = re.sub(r'<\?xml[^>]+\?>\s*', '', svg)
    wrapper = f'<div style="margin: 1.2rem 0;">{svg}</div>'
    # Insert before the section's closing </section>
    pattern = f'(<section id="{section_id}"[\\s\\S]*?)</section>'
    guide_html = re.sub(pattern, r'\1' + wrapper + '</section>', guide_html, count=1)

# Add respiratory svg too — insert it right after the heart one in topic-7
resp_svg = svg_inline.get("03_respiratory_path", "")
if resp_svg:
    resp_svg_clean = re.sub(r'<\?xml[^>]+\?>\s*', '', resp_svg)
    resp_wrapper = f'<div style="margin: 1.2rem 0;">{resp_svg_clean}</div>'
    # Insert in topic-7 after the heart svg we already inserted
    guide_html = guide_html.replace(
        svg_inline["02_heart_blood_flow"].replace('<?xml version="1.0" encoding="UTF-8"?>\n', ''),
        svg_inline["02_heart_blood_flow"].replace('<?xml version="1.0" encoding="UTF-8"?>\n', '') + resp_wrapper,
        1
    )

(SD / "00_START_HERE.html").write_text(guide_html)
print(f"Wrote {SD / '00_START_HERE.html'}")

# ---------- 2. PDFs from HTML ----------
def html_to_pdf(html_path: Path, pdf_path: Path):
    HTML(string=html_path.read_text(), base_url=str(html_path.parent)).write_pdf(str(pdf_path))
    print(f"Wrote {pdf_path}")

html_to_pdf(SD / "00_START_HERE.html", SD / "Chloe_Study_Guide.pdf")
html_to_pdf(RUN / "cheat_sheet.html", SD / "Chloe_Cheat_Sheet.pdf")

# ---------- 3. Markdown → HTML → PDF, and Markdown → DOCX ----------

MD_CSS = """
@page { size: letter; margin: 0.6in 0.7in; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
       font-size: 10.5pt; line-height: 1.4; color: #1c1c1c; }
h1 { color: #1f6f3f; font-size: 18pt; border-bottom: 2px solid #1f6f3f; padding-bottom: 4px; }
h2 { color: #1f6f3f; font-size: 13pt; margin-top: 16pt; }
h3 { color: #2a4d7a; font-size: 11pt; margin-top: 10pt; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0; font-size: 9.5pt; }
th, td { border: 1px solid #aaa; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { background: #d4ead7; }
code { font-family: "SF Mono", "Menlo", Consolas, monospace; background: #f0ede4; padding: 1pt 3pt; border-radius: 2pt; font-size: 9pt; }
ul, ol { margin: 4pt 0; padding-left: 18pt; }
strong { color: #14492c; }
blockquote { border-left: 3px solid #1f6f3f; padding-left: 10pt; color: #444; font-style: italic; }
hr { border: none; border-top: 1px solid #ddd; margin: 12pt 0; }
"""

def md_to_pdf(md_path: Path, pdf_path: Path, css=MD_CSS):
    md_text = md_path.read_text()
    html_body = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    full_html = f"<html><body>{html_body}</body></html>"
    HTML(string=full_html).write_pdf(str(pdf_path), stylesheets=[CSS(string=css)])
    print(f"Wrote {pdf_path}")

md_to_pdf(RUN / "study_plan.md", SD / "Chloe_Study_Plan.pdf")
md_to_pdf(RUN / "glossary.md",   SD / "Chloe_Glossary.pdf")
md_to_pdf(RUN / "quiz_bank.md",  SD / "Chloe_Quiz_Bank.pdf")

# ---------- 4. Markdown → DOCX (using simple md → docx via python-docx) ----------

def md_to_docx(md_path: Path, docx_path: Path):
    md_text = md_path.read_text()
    doc = Document()
    # default styles
    style = doc.styles["Normal"]
    style.font.name = "Helvetica"
    style.font.size = Pt(11)

    lines = md_text.split("\n")
    i = 0
    in_table = False
    table_rows = []

    def flush_table():
        nonlocal table_rows
        if not table_rows:
            return
        cols = len(table_rows[0])
        t = doc.add_table(rows=len(table_rows), cols=cols)
        t.style = "Light Grid Accent 1"
        for r_idx, row in enumerate(table_rows):
            for c_idx, cell in enumerate(row):
                t.rows[r_idx].cells[c_idx].text = cell
        table_rows = []

    while i < len(lines):
        line = lines[i].rstrip()
        # Skip table separator lines like |---|---|
        if re.match(r'^\s*\|[\s\-:|]+\|\s*$', line):
            i += 1
            continue
        # Table row
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            # strip markdown bold from each cell for docx simplicity
            cells = [re.sub(r'\*\*(.+?)\*\*', r'\1', c) for c in cells]
            cells = [re.sub(r'`(.+?)`', r'\1', c) for c in cells]
            table_rows.append(cells)
            in_table = True
            i += 1
            continue
        else:
            if in_table:
                flush_table()
                in_table = False

        if not line.strip():
            i += 1
            continue

        # Headings
        if line.startswith("### "):
            doc.add_heading(line[4:], level=3)
        elif line.startswith("## "):
            doc.add_heading(line[3:], level=2)
        elif line.startswith("# "):
            doc.add_heading(line[2:], level=1)
        elif line.startswith("---"):
            doc.add_paragraph("")
        elif re.match(r'^\s*[-*]\s', line):
            text = re.sub(r'^\s*[-*]\s', '', line)
            text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
            text = re.sub(r'`(.+?)`', r'\1', text)
            doc.add_paragraph(text, style="List Bullet")
        elif re.match(r'^\s*\d+\.\s', line):
            text = re.sub(r'^\s*\d+\.\s', '', line)
            text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
            text = re.sub(r'`(.+?)`', r'\1', text)
            doc.add_paragraph(text, style="List Number")
        else:
            text = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
            text = re.sub(r'`(.+?)`', r'\1', text)
            text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
            doc.add_paragraph(text)
        i += 1

    if in_table:
        flush_table()
    doc.save(str(docx_path))
    print(f"Wrote {docx_path}")

md_to_docx(RUN / "study_plan.md", SD / "Chloe_Study_Plan.docx")
md_to_docx(RUN / "glossary.md",   SD / "Chloe_Glossary.docx")
md_to_docx(RUN / "quiz_bank.md",  SD / "Chloe_Quiz_Bank.docx")

# ---------- 5. Flashcards → just copy ----------
shutil.copy(RUN / "flashcards.txt", SD / "Chloe_Flashcards.txt")
print(f"Wrote {SD / 'Chloe_Flashcards.txt'}")

# ---------- 6. Each SVG → individual PDF ----------
for svg_path in sorted(VIS.glob("*.svg")):
    svg_text = svg_path.read_text()
    html = f"<html><body style='margin:0;padding:8pt'>{svg_text}</body></html>"
    out_pdf = DIAG / (svg_path.stem + ".pdf")
    HTML(string=html, base_url=str(svg_path.parent)).write_pdf(str(out_pdf),
        stylesheets=[CSS(string="@page { size: letter landscape; margin: 0.3in; }")])
    print(f"Wrote {out_pdf}")

# ---------- 7. Consolidated PRINT PACK ----------
# Cover + TOC + study plan + glossary + study guide + cheat sheet + quiz bank
# Each as its own PDF, then merge with fitz.

cover_html = """
<html><head><style>
@page { size: letter; margin: 0.7in; }
body { font-family: -apple-system, Helvetica, sans-serif; text-align: center; color: #1c1c1c; }
h1 { color: #1f6f3f; font-size: 32pt; margin-top: 2.5in; }
.sub { font-size: 16pt; color: #444; margin-top: 1rem; }
.date { font-size: 14pt; color: #b1530a; font-weight: 700; margin-top: 1rem; }
.toc { text-align: left; margin: 2in 1in 0; font-size: 12pt; line-height: 2; }
.toc h2 { color: #1f6f3f; font-size: 18pt; border-bottom: 2px solid #1f6f3f; }
.howto { text-align: left; margin: 1in; font-size: 11pt; color: #444; line-height: 1.5; }
.howto h2 { color: #2a4d7a; }
</style></head><body>
<h1>Chloe's Biology Final<br>Complete Study Pack</h1>
<div class="sub">9th Grade Biology · Final Exam Review</div>
<div class="date">Friday, May 29, 2026 · 1–3 PM<br>North Gym</div>
<div class="date">Teachers: Bertram · Deasy · Seatter</div>
<div style="page-break-after: always;"></div>

<h2 style="color:#1f6f3f; font-size: 22pt; margin-top: 0.4in;">What's in this pack</h2>
<div class="toc">
<p>1. Study Plan — your 13-day schedule</p>
<p>2. Glossary — every term from the review guide</p>
<p>3. Study Guide — comprehensive content for all 7 topics</p>
<p>4. Cheat Sheet — 2 pages, for the night before / morning of</p>
<p>5. Quiz Bank — 60+ practice questions with answers</p>
</div>

<div class="howto">
<h2>How to use this pack</h2>
<p><b>Print it.</b> Staple it. Carry it. The interactive version is on your phone/laptop, but this is the one-document version for studying offline at the kitchen table.</p>
<p><b>Follow the study plan.</b> Spread study time across 13 days — don't cram. Your teacher recommended at least 20 minutes per night starting May 17.</p>
<p><b>Use the cheat sheet only on May 28–29.</b> It's a recall trigger, not a learning tool.</p>
<p><b>Watch-Out callouts</b> in orange are common test traps. Pay extra attention.</p>
<p><b>Teacher-specified exclusion:</b> SKIP Hardy-Weinberg / Genetic Equilibrium. NOT on the exam.</p>
</div>
</body></html>
"""
cover_pdf = SD / "_tmp_cover.pdf"
HTML(string=cover_html).write_pdf(str(cover_pdf))

# Build study guide PDF for inclusion in the pack (the standalone guide is interactive; reuse the same file)
# We already wrote SD / "Chloe_Study_Guide.pdf" above.

# Compact-style overlay for study plan / glossary / quiz: re-render with tighter CSS to keep page budget
COMPACT_CSS = MD_CSS + """
@page { size: letter; margin: 0.45in 0.55in; }
body { font-size: 9.5pt; line-height: 1.3; }
h1 { font-size: 15pt; margin-top: 0; }
h2 { font-size: 11pt; margin-top: 10pt; }
h3 { font-size: 10pt; }
table { font-size: 8.5pt; }
th, td { padding: 2.5pt 4pt; }
ul, ol { margin: 3pt 0; }
"""

tmp = {}
for name in ("study_plan", "glossary", "quiz_bank"):
    tmp_pdf = SD / f"_tmp_{name}.pdf"
    md_to_pdf(RUN / f"{name}.md", tmp_pdf, css=COMPACT_CSS)
    tmp[name] = tmp_pdf

# Make a slimmed-down study guide HTML (drop the sticky nav and shrink fonts) for the print pack
guide_compact = guide_html
# Remove sticky nav to free vertical space
guide_compact = re.sub(r'<nav[\s\S]*?</nav>', '', guide_compact, count=1)
# Tighten body font
guide_compact = guide_compact.replace(
    'body { margin: 0; padding: 0; background: var(--bg); color: var(--ink); font-family:',
    'body { margin: 0; padding: 0; background: white; color: var(--ink); font-family:'
)
# Add print CSS
print_css = """
<style>
  @page { size: letter; margin: 0.4in 0.5in; }
  body { font-size: 8.6pt !important; line-height: 1.25 !important; }
  .wrapper { max-width: none !important; padding: 0 !important; }
  header { padding-bottom: 4pt !important; margin-bottom: 5pt !important; }
  h1 { font-size: 13pt !important; }
  .subtitle { font-size: 9pt !important; }
  section { padding: 5pt 7pt !important; margin-bottom: 5pt !important; border: 1px solid #ccc !important; box-shadow: none !important; page-break-inside: avoid; }
  section > h2 { font-size: 11pt !important; margin-top: 0 !important; padding-bottom: 1pt !important; }
  h3 { font-size: 9.4pt !important; margin-top: 4pt !important; margin-bottom: 1pt !important; }
  h4 { font-size: 8.8pt !important; margin-top: 3pt !important; margin-bottom: 1pt !important; }
  p { margin: 2pt 0 !important; }
  table { font-size: 7.6pt !important; margin: 3pt 0 !important; }
  th, td { padding: 1.5pt 3pt !important; }
  .callout { padding: 3pt 5pt !important; font-size: 8pt !important; margin: 3pt 0 !important; }
  details.quiz { padding: 3pt 5pt !important; margin: 3pt 0 !important; }
  details.quiz summary { font-size: 8.2pt; }
  details.quiz .answer { font-size: 8pt; }
  details.quiz { display: block; }
  details.quiz > *:not(summary) { display: block !important; }
  .exclusion { padding: 3pt 5pt !important; font-size: 8.2pt !important; margin: 4pt 0 !important; }
  .key-fact { padding: 3pt 5pt !important; font-size: 8.2pt !important; margin: 3pt 0 !important; }
  footer { display: none; }
  nav { display: none; }
  ul, ol { margin: 2pt 0 !important; padding-left: 14pt !important; }
  li { margin-bottom: 1pt !important; }
  svg { max-width: 70% !important; height: auto !important; display: block; margin: 3pt auto !important; max-height: 220pt !important; }
  pre { font-size: 7.5pt !important; padding: 3pt !important; margin: 3pt 0 !important; }
  /* Pack: hide section IDs we don't need duplicated */
  #how-to-use { display: none; }
</style>
"""
guide_compact = guide_compact.replace("</head>", print_css + "</head>")

guide_compact_path = SD / "_tmp_guide_compact.html"
guide_compact_path.write_text(guide_compact)
guide_compact_pdf = SD / "_tmp_guide_compact.pdf"
HTML(string=guide_compact, base_url=str(SD)).write_pdf(str(guide_compact_pdf))
print(f"Wrote {guide_compact_pdf}")

# Now stitch them together with fitz. Per skill: if natural content > 25 pages,
# split into pack + separate reference (glossary, quiz). Pack = cover + plan + guide + cheat.
pack_pdf = SD / "Chloe_Biology_Complete.pdf"
out_doc = fitz.open()
for piece in [cover_pdf, tmp["study_plan"], guide_compact_pdf, SD / "Chloe_Cheat_Sheet.pdf"]:
    src = fitz.open(str(piece))
    out_doc.insert_pdf(src)
    src.close()
out_doc.save(str(pack_pdf))
out_doc.close()
print(f"Wrote {pack_pdf}")

# Also rebuild Chloe_Study_Guide.pdf using the COMPACT version so the standalone
# guide PDF respects the 25-page hard cap. (00_START_HERE.html stays full-feature
# for browser viewing.)
shutil.copy(guide_compact_pdf, SD / "Chloe_Study_Guide.pdf")
print(f"Replaced Chloe_Study_Guide.pdf with compact version")

# Cleanup temp pieces
for f in list(SD.glob("_tmp_*")):
    f.unlink()

# Report final page counts
for label, p in [
    ("Study Guide PDF", SD / "Chloe_Study_Guide.pdf"),
    ("Cheat Sheet", SD / "Chloe_Cheat_Sheet.pdf"),
    ("Study Plan", SD / "Chloe_Study_Plan.pdf"),
    ("Glossary", SD / "Chloe_Glossary.pdf"),
    ("Quiz Bank", SD / "Chloe_Quiz_Bank.pdf"),
    ("CONSOLIDATED PACK", pack_pdf),
]:
    d = fitz.open(str(p))
    print(f"  {label}: {len(d)} pages")
    d.close()
