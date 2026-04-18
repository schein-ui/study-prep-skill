# Phase 1: Intake

## Goal

Establish the run directory, catalog all materials, confirm test scope + format + exclusions, and write the handoff note that downstream phases read.

## Steps

### 1. Create run directory

```
{working_dir}/study-prep-output/{run-id}/
{working_dir}/study-prep-state/{run-id}/
```

`{run-id}` format: `YYYY-MM-DD_<subject-slug>`. The subject slug is 1-2 words, lowercase, hyphen-separated (e.g., `evolution`, `civil-war`, `quadratics`).

### 2. Catalog materials (what did the user provide?)

Accept any of:
- **A zip** of teacher materials — unzip to `{state}/source_materials/`
- **Individual PDFs** — copy or link into `{state}/source_materials/`
- **Paths to files already on disk** — note the paths; don't copy unless the user requests
- **Student's completed work** — keep separate from teacher materials so the audit phase knows which is which
- **A handoff prompt.txt** or prior-conversation summary — read it fully; it may contain locked constraints

Print a catalog back to the user:

```
MATERIALS CATALOG
Teacher materials:
  - <file1.pdf> (N pages)
  - <file2.pptx.pdf> (N pages)
Student work:
  - <student reading guide 1.pdf>
  - <student reading guide 2.pdf>
Other:
  - <handoff prompt.txt>
Test: <subject>, <date>, <format>
Excluded topics: <any>
```

### 3. Confirm test scope with the user

The scope determines what's in and out. Before producing anything, surface:

- **Chapters/units in scope:** list them explicitly
- **Explicitly excluded topics:** if the teacher said "skip X," write it down. Teachers commonly exclude sections to save time; honor it.
- **Test format:** MC / SA / diagram / FRQ / essay — each affects deliverable weighting
- **On-the-test-for-sure items:** specific figures, tables, mnemonics, readings the teacher flagged
- **Prior quizzes or reviews:** the teacher's past test items predict current test items

Ask the user to confirm scope if any of these are unclear. Do NOT guess at exclusions — guessing about what's excluded is the most expensive error to make.

### 4. Capture student profile

One paragraph. Useful signals:

- Grade level (affects language register)
- Known learning-style preferences (visual/kinesthetic/reading-writing/auditory; ADHD, dyslexia, ESL, gifted)
- Prior performance in this subject (confident vs. anxious)
- Any specific misconceptions the parent has noticed
- Name (use in direct-address copy; "Welcome, Chloe" beats "Welcome, student")

Don't invent a profile. If you don't know, say so and proceed with generic-but-age-appropriate language.

### 5. Resolve agentloop interaction

study-prep **uses** agentloop, not reimplements it. At intake:

- Determine whether to run a full agentloop Phase 1+2 (casting + roundtable), OR skip directly to Execution if the user has supplied a complete scoping/roundtable handoff.
- If the user provides a locked execution plan (like a prompt.txt with T1-T8 tasks), skip agentloop Phase 1/2, proceed to Phase 3 Execution with those tasks.
- If the user just says "my kid has a test, help," run agentloop Phase 1/2 first.

### 6. Write the handoff

Write `{state}/handoff_intake.md`:

```markdown
# Intake → Primary-Source Handoff

## Run
- Run ID: <id>
- Working dir: <path>
- Created: <ISO date>

## Subject
<subject>, <grade level>, <student name>

## Test
- Date: <ISO date>
- Format: <MC + SA + ...>
- Days until test: <N>
- Excluded topics (verbatim from teacher if provided): <list or "none">

## Teacher materials
<list with N pages each>

## Student work to audit
<list>

## User directives / locked constraints
<anything the user said can't change>

## Student profile
<1 paragraph>

## agentloop mode
full (run casting + roundtable) | skip (user provided locked plan)

## Open questions the user didn't answer
<list — if non-empty, ask before proceeding to Phase 2>
```

If any open question is load-bearing (especially scope/exclusions), STOP and ask before proceeding.

## Output of this phase

- Run directories created
- All materials cataloged
- Scope confirmed
- Handoff note written
- User has either confirmed scope or answered open questions

## Checklist before proceeding to primary-source

```
[ ] Run directories exist
[ ] Every provided file is accounted for (teacher / student / handoff)
[ ] Scope + exclusions confirmed in writing
[ ] Test date is absolute, not relative ("Tuesday" → "2026-04-21")
[ ] Student profile captured or explicitly marked unknown
[ ] handoff_intake.md written
[ ] No load-bearing open questions
```
