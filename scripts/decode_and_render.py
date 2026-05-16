#!/usr/bin/env python3
"""Decode the saved base64 Drive download into a real PDF, then render selected pages."""
import json, base64, sys
from pathlib import Path
import fitz

SAVED = sys.argv[1]            # path to the tool-results .txt
OUTPDF = sys.argv[2]           # where to save decoded PDF
PAGES  = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else []

data = json.loads(Path(SAVED).read_text())
pdf_bytes = base64.b64decode(data["content"])
Path(OUTPDF).write_bytes(pdf_bytes)
print(f"Wrote {OUTPDF} ({len(pdf_bytes):,} bytes)")

# Render specified pages (1-indexed) to PNG
if PAGES:
    out_dir = Path(OUTPDF).with_suffix("")
    out_dir.mkdir(exist_ok=True)
    d = fitz.open(OUTPDF)
    print(f"PDF has {len(d)} pages")
    for p in PAGES:
        if 1 <= p <= len(d):
            page = d[p-1]
            pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
            out = out_dir / f"page_{p:03d}.png"
            pix.save(str(out))
            print(f"  rendered page {p} → {out}")
    d.close()
