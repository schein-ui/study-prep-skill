# Phase 3: Student-Work Audit

## Goal

Find every error in the student's own completed work and turn each one into a "Watch Out!" card. This is the **single highest-leverage move in the entire skill**. The student has been studying with wrong answers since they submitted the homework; if you don't surface those errors, they'll walk into the test reinforcing the wrong version.

## Why this matters

Teachers commonly grade homework for completion, not accuracy. A student can submit a reading guide with 7 wrong answers and get full credit. The student now believes those 7 wrong answers are right.

Research backs refutation text: seeing the wrong belief and the correct version together overwrites the wrong belief more reliably than seeing only the correct version. That's why "Errors in My Notes" must appear FIRST in the study path, not buried in an appendix.

## Protocol

### 1. Read every question and answer

For each item in the student's completed work:
- What was the question?
- What did the student write?
- What's the correct answer (per the primary source)?
- Are they the same?

Don't skim. Typos and word-mixups are high-severity and easy to skip past.

### 2. Classify each answer

| Classification | Example |
|----------------|---------|
| **CORRECT** | Answer matches the primary source |
| **HIGH** — factual error | Wrong word, wrong concept, wrong definition |
| **MEDIUM** — imprecise but on-track | Incomplete, missing key detail, close-but-not-exact |
| **LOW** — spelling/typo | Concept correct, surface error |
| **INCOMPLETE** | Question skipped or answered partially (e.g., asked for 2 examples, gave 1) |

### 3. For each HIGH/MEDIUM, record

```
Error #N
  Location: Ch 17, Lesson 17.2, Question 4
  Student wrote: "inheritance of acquired TASTE"
  Correct: "inheritance of acquired CHARACTERISTICS"
  Severity: HIGH
  Why it matters: Lamarck's exact phrase, which the test will likely quote verbatim.
                  Confusing "taste" for "characteristics" = missing the actual concept.
  Common wrong-pattern: typo that reads plausibly, student didn't re-check.
```

### 4. Look for error patterns

Common pilot-run findings:
- **Word-mixups from similar-sounding terms** — "polygenic" vs. "phylogenetic," "cavitation" vs. "variation," "alopartic" vs. "allopatric." These are almost always intentional test distractors.
- **Copy-paste errors** — student pasted the previous answer into a new question.
- **Circular definitions** — "X is the study of how X happens." Teacher likely scored full credit; it's still wrong.
- **Factually wrong answers** — e.g., wrong date, wrong count, wrong species.
- **Blank answers** — question wasn't completed.
- **Misspellings of proper nouns** — "Glatodont" for "Glyptodont"; loses credit on written answers even if concept is right.

### 5. Write the errors file

Output: `{output}/errors_in_notes.md`:

```markdown
# Errors in <Student>'s Reading Guide / Notes

Summary: N errors found (X HIGH, Y MEDIUM, Z LOW/SPELLING).

## Error 1 — HIGH — Ch 17 L17.2 Q4
Student wrote: "inheritance of acquired TASTE"
Correct: "inheritance of acquired CHARACTERISTICS"
Why: <explanation>

## Error 2 — ...
```

This file gets referenced by every downstream deliverable. The "Errors in My Notes" section of the interactive study guide renders these as red cards.

### 6. Silently correct body content

When the error appears in ANY other deliverable (glossary, study guide, quiz, cheat sheet):
- **Use the correct answer.** Don't repeat the student's wrong version in the main content.
- **Surface the wrong version ONLY in the "Errors in My Notes" section.**

Reason: we want the student to encounter the wrong version exactly once, with its correction adjacent. Re-showing it in body content reinforces it.

### 7. Build quiz distractors from the student's actual errors

If the student wrote "cavitation" for "variation" in a reading guide, the MC question about NS conditions should include "cavitation" as option D. That converts their specific confusion into a targeted test-prep item.

Every HIGH error → at least one quiz item with the wrong version as a distractor.

## Completeness check

The audit is complete when:

```
[ ] Every question in every piece of student work has been read
[ ] Every answer classified (correct / HIGH / MEDIUM / LOW / incomplete)
[ ] Every HIGH error has location + wrote + correct + why
[ ] Every MEDIUM error has the same
[ ] errors_in_notes.md written
[ ] Quiz distractors being generated from HIGH errors (tracked for Phase 4)
```

If you can't locate the exact page/question for an error, flag it — the student needs to know where to look in their own notes to fix it.

## Anti-patterns

- ❌ "The teacher already graded this, so it's fine." The teacher likely graded for completion. Verify.
- ❌ Skimming the student's work. Read carefully — typos are high-severity.
- ❌ Deciding an error is "too minor." If the student wrote the wrong word, flag it. Spelling counts on written tests.
- ❌ Listing errors but not building quiz distractors from them. The distractor is the teaching moment.
