#!/usr/bin/env python3
"""Render QC report and Grading Scorecard as PDFs into for_parent/."""
from pathlib import Path
import markdown
from weasyprint import HTML, CSS

ROOT = Path(__file__).resolve().parent.parent
RUN = ROOT / "study-prep-output" / "2026-05-29_biology-final"
PARENT = RUN / "for_parent"
PARENT.mkdir(parents=True, exist_ok=True)

CSS_STR = """
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

for md_name, pdf_name in [("qc_report.md", "QC_Report.pdf"),
                          ("grading_scorecard.md", "Grading_Scorecard.pdf")]:
    md = (RUN / md_name).read_text()
    html_body = markdown.markdown(md, extensions=["tables", "fenced_code"])
    HTML(string=f"<html><body>{html_body}</body></html>").write_pdf(
        str(PARENT / pdf_name), stylesheets=[CSS(string=CSS_STR)]
    )
    print(f"Wrote {PARENT / pdf_name}")
