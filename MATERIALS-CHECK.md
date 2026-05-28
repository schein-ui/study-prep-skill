---
name: materials-check
description: Verify that downloaded study materials (from cloudclass.ai or any school portal) are complete and ready for study-prep. Scans a directory, checks file integrity, categorizes materials, and produces a readiness report with GREEN/YELLOW/RED status.
---

# materials-check

## What this skill does

Before running `study-prep`, you need to make sure all the right materials are downloaded from the school portal (cloudclass.ai, Google Classroom, Canvas, etc.). This skill:

1. **Pre-download**: Creates the run directory and prints a checklist of what to download
2. **Post-download**: Scans the materials directory, verifies file integrity, categorizes everything, and produces a readiness report
3. **Hands off** to `study-prep` with a preliminary handoff note so Phase 1 doesn't re-ask questions

## When to invoke

- User says "check materials", "are the materials ready", "verify downloads", "what do I need to download"
- User says "check [student]'s [subject]" or "is [unit] ready"
- Before running study-prep, as a pre-flight
- User asks "do I have everything for [student]'s test"

Do NOT invoke for:
- Actually building the study guide (use `study-prep`)
- Downloading materials on behalf of the user (manual download only)

## Inputs you collect

| Input | Required? | Example |
|-------|-----------|---------|
| **Student name** | Yes | Ryder |
| **Grade** | Yes | 7th |
| **Subject** | Yes | Science |
| **Unit/topic** | Yes | Unit 7 |
| **Test date** | Optional | 2026-06-05 |
| **Materials path** | Optional — auto-create if omitted | study-prep-state/2026-06-05_science-unit7/source_materials/ |

If the user provides partial info (e.g., "check Ryder's science"), ask for the missing pieces before proceeding.

## Phase A — Pre-Download Guidance

Run this phase when the user says materials are NOT yet downloaded, or when the materials directory is empty.

### Step 1: Create the run directory

Use the standard convention from `study-prep`:

```
{repo_root}/study-prep-state/{YYYY-MM-DD}_{subject-slug}/source_materials/
```

Use test date if provided; otherwise use today's date. The subject slug is lowercase, hyphen-separated, and includes the unit (e.g., `science-unit7`, `history-ch12`, `algebra-midterm`).

```bash
mkdir -p study-prep-state/{run-id}/source_materials
```

### Step 2: Print the download checklist

```
╔══════════════════════════════════════════════════════════════╗
║  CLOUDCLASS DOWNLOAD CHECKLIST                              ║
║  {Student} · {Grade} {Subject} · {Unit}                     ║
╚══════════════════════════════════════════════════════════════╝

Go to cloudclass.ai (or your school portal) and download
ALL of the following that exist for this unit:

  □  Slide decks / lecture presentations (PPT or PDF)
  □  Reading guides — blank teacher version
  □  Reading guides — student's COMPLETED version
  □  Worksheets / practice problems
  □  Answer keys (if available to parents)
  □  Lab reports or activity sheets
  □  Review guide / study guide from the teacher
  □  Previous quizzes or tests on this unit
  □  Supplementary handouts or reference sheets
  □  Video links (paste URLs into a notes.txt file)

Download destination:
  {absolute_path_to_source_materials}/

Tips:
  • Use bulk export / "download all" if cloudclass has it
  • Unzip directly into the folder above
  • Include BOTH blank and completed versions of worksheets
  • Student's completed work is critical — it drives the error audit
```

### Step 3: Wait for confirmation

Tell the user: "Download the materials into that folder, then tell me when you're done and I'll verify everything."

When the user confirms, proceed to Phase B.

## Phase B — Post-Download Verification

Run this phase when materials exist in the directory (user says "I downloaded them" or files are detected).

### Step 1: File inventory

Scan the source_materials directory and build an inventory:

```bash
find {source_materials_path} -type f | sort
```

For each file, collect:
- **Filename** and extension
- **Size** (human-readable)
- **MIME type** via `file --mime-type`
- **PDF page count** (if PDF):
  ```python
  python3 -c "
  import sys
  try:
      import fitz
      doc = fitz.open(sys.argv[1])
      print(len(doc))
  except:
      try:
          import subprocess
          r = subprocess.run(['pdfinfo', sys.argv[1]], capture_output=True, text=True)
          for line in r.stdout.splitlines():
              if line.startswith('Pages:'):
                  print(line.split(':')[1].strip())
                  break
      except:
          print('?')
  " "$file"
  ```

Print a formatted table:

```
MATERIALS INVENTORY
═══════════════════════════════════════════════════════════════
 #  Filename                                    Type    Size    Pages
 1  Evolution_Slides.pdf                        PDF     2.1 MB  45
 2  Unit7_Reading_Guide.pdf                     PDF     180 KB  6
 3  Unit7_Reading_Guide_Ryder.pdf               PDF     4.8 MB  6
 4  Lab_Report_Cells.pdf                        PDF     95 KB   3
 5  review_sheet.docx                           DOCX    42 KB   —
 6  diagram.png                                 Image   1.2 MB  —
─────────────────────────────────────────────────────────────
 Total: 6 files · 8.4 MB
```

### Step 2: Integrity checks

For every PDF:

```python
python3 -c "
import fitz, sys, os
path = sys.argv[1]
try:
    doc = fitz.open(path)
    pages = len(doc)
    size = os.path.getsize(path)
    if size < 5000:
        print(f'⚠️  WARN: {os.path.basename(path)} — only {size} bytes, may be empty/corrupt')
    elif pages == 0:
        print(f'❌ FAIL: {os.path.basename(path)} — 0 pages')
    else:
        print(f'✅ OK: {os.path.basename(path)} — {pages} pages')
    doc.close()
except Exception as e:
    print(f'❌ FAIL: {os.path.basename(path)} — cannot open: {e}')
" "$file"
```

Also check:
- **Zero-byte files**: `find {path} -empty -type f`
- **Duplicate content**: files with identical sizes (flag for review, don't auto-delete)
- **Non-standard formats**: anything that isn't PDF/DOCX/PPTX/PNG/JPG/TXT — flag but don't reject

### Step 3: Categorize materials

Use filename heuristics to classify each file. Match case-insensitively against these patterns:

| Category | Filename patterns | Priority |
|----------|------------------|----------|
| **Slides/Lectures** | slide, ppt, lecture, notes, lesson, "+S" suffix, numbered presentations | HIGH |
| **Reading Guides (teacher)** | reading guide, RG, chapter + guide (without student name) | HIGH |
| **Reading Guides (student)** | reading guide + student name, completed, filled, scanned | CRITICAL |
| **Worksheets/Practice** | worksheet, WS, practice, activity, lab, exercise | MEDIUM |
| **Answer Keys** | key, answer, solution, KEY suffix | MEDIUM |
| **Review/Study Guide** | review, study guide, final review, test prep, exam review | HIGH |
| **Quizzes/Tests** | quiz, test, assessment, exam (prior unit) | MEDIUM |
| **Reference** | reference, handout, supplement, chart, table | LOW |
| **Images** | .png, .jpg, .jpeg, .gif, .svg | LOW |
| **Video/Links** | .mp4, .mov, notes.txt with URLs | LOW |
| **Unknown** | anything else | — ask user |

If a file doesn't match any pattern, ask the user: "I can't tell what `{filename}` is — is it teacher materials, student work, or something else?"

### Step 4: Completeness assessment

Score each category as present or absent and produce the readiness report:

```
╔══════════════════════════════════════════════════════════════╗
║  READINESS REPORT                                           ║
║  {Student} · {Grade} {Subject} · {Unit}                     ║
╚══════════════════════════════════════════════════════════════╝

Files: {N} files · {total_size}
PDFs:  {passed}/{total_pdfs} passed integrity check

CATEGORY CHECKLIST:
  ✅  Slides/lectures ············ {count} files ({pages} total pages)
  ✅  Reading guides (teacher) ··· {count} files
  ❌  Reading guides (student) ·· NONE FOUND
  ✅  Worksheets/practice ········ {count} files
  ⚠️   Answer keys ·············· NONE FOUND
  ✅  Review guide ··············· {count} files
  ⚠️   Prior quizzes ············ NONE FOUND

ISSUES:
  ❌  corrupt_file.pdf — cannot open (0 bytes)
  ⚠️   tiny_file.pdf — only 3 KB, may be incomplete

OVERALL STATUS: 🟡 YELLOW — Can proceed but missing student work
```

**Status logic:**
- 🟢 **GREEN** — Has slides/lectures + teacher reading guides/worksheets + student completed work + at least one review guide or answer key. All PDFs pass integrity. Ready for study-prep.
- 🟡 **YELLOW** — Has teacher materials but missing student completed work OR missing answer keys. Can run study-prep but the error audit will be limited.
- 🔴 **RED** — Missing teacher materials entirely (no slides, no reading guides), OR all PDFs are corrupt, OR directory is empty. Cannot proceed until more materials are downloaded.

**Recommendations section:**

Based on what's missing, print specific next steps:

```
RECOMMENDATIONS:
  1. ❌ Download {Student}'s completed reading guides from cloudclass
     → The error audit (study-prep Phase 3) needs these — it's the
       highest-leverage input for the study guide
  2. ⚠️  Check if answer keys are available for this unit
     → Improves verification accuracy in Phase 2
  3. ✅ You have enough to start — invoke study-prep when ready

NEXT STEP: [specific instruction based on status]
```

### Step 5: Write preliminary handoff note

If status is GREEN or YELLOW, write `{state}/handoff_intake_draft.md`:

```markdown
# Handoff — Materials Check (Draft)

**Student:** {name}
**Grade:** {grade}
**Subject:** {subject}
**Unit/Topic:** {unit}
**Test date:** {date or "TBD"}
**Run ID:** {run-id}

## Materials on disk
{inventory table from Step 1}

## Categories
- Slides/lectures: {list}
- Reading guides (teacher): {list}
- Reading guides (student): {list or "MISSING"}
- Worksheets: {list}
- Answer keys: {list or "MISSING"}
- Review guide: {list or "MISSING"}

## Known gaps
{list of missing categories or "None — all categories present"}

## Status
{GREEN/YELLOW/RED} — {one-line summary}

## Notes for study-prep Phase 1
- Materials path: {absolute path}
- This is a draft — study-prep Phase 1 should verify and expand
```

Name it `handoff_intake_draft.md` (not `handoff_intake.md`) so study-prep Phase 1 knows it's preliminary and can overwrite it with the full version.

## Composition with study-prep

This skill's output feeds directly into `study-prep` Phase 1:

1. **Directory structure** — already created in the convention study-prep expects
2. **Handoff draft** — study-prep reads it for context, then writes the full `handoff_intake.md`
3. **Readiness status** — tells the parent whether to download more or proceed

After `materials-check` gives GREEN or YELLOW:
> "Materials look good. Run study-prep to start building the study guide."

After RED:
> "You're missing critical materials. Here's what to download: [specific list]"
