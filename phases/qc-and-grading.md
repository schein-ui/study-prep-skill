# Phase 5: QC + Grading Loop

## Goal

Verify the bundle is complete, accurate, aligned to primary sources, and meets the user's quality target — **honestly**, with retrospective acknowledgment of any inflation from earlier passes.

## Grading criteria (6)

| # | Criterion | Owner | What it tests |
|---|-----------|-------|---------------|
| 1 | **Content Accuracy** | Domain specialist | Facts correct; no misconceptions; tables and figures exact |
| 2 | **Curriculum Fit** | Subject teacher | Matches teacher's syllabus + slides + stated scope; exclusions honored |
| 3 | **Pedagogy** | Learning scientist | Retrieval practice, interleaving, refutation text, appropriate reading level |
| 4 | **Assessment Quality** | Assessment specialist | Distractors from student's actual errors; rubric-style scoring targets |
| 5 | **Engagement** | Learning scientist + Teacher | Direct voice, visual support, urgency markers for errors |
| 6 | **Cross-Deliverable Consistency** | Skeptic | Same definitions, numbers, examples across all files |

Target: all 6 at **A- or above**. This is the default per agentloop conventions. Some runs may target A or A+; user sets it.

## QC protocol

Before the first grading pass, run QC checks:

```
QC CHECKLIST

[ ] Every HIGH error from audit is surfaced AND silently corrected
[ ] Every exclusion (teacher said "skip X") honored in every deliverable — grep for the excluded term
[ ] Numerical tables match primary source verbatim (row-by-row, cell-by-cell)
[ ] Key mnemonics match teacher's exact phrasing
[ ] 4+-part lists match the teacher's count (3 domains, 4 kingdoms, etc.)
[ ] Cross-file consistency: grep same term across all files, compare definitions
[ ] Standalone HTML renders offline — open and verify
[ ] Cheat sheet is exactly 2 pages — open the PDF and verify
[ ] No .jsx / .md-only / framework-dependent artifacts in student_downloads/
```

Write results to `qc_report.md`.

## Grading loop — anti-inflation mandatory

Each pass produces a scorecard entry. If a later pass finds a gap, retrospectively downgrade earlier passes in writing.

### Per-pass structure

```markdown
## Pass N

| # | Criterion | Grade | Evidence |
|---|-----------|-------|----------|
| 1 | Content Accuracy | <letter> | <specific evidence: "verified cytochrome C table row-by-row against slide 36" or "missed teacher's bee/bat analogous example, now caught" |
| 2 | Curriculum Fit | <letter> | ... |
| ... | ... | ... | ... |

**Pass N floor:** <lowest grade>
**Pass N average:** <avg>
**Pass N verdict:** PASS / REVISE
```

### Retrospective structure (only if a later pass finds a gap)

```markdown
## Honest Pass N retrospective

<What earlier pass's grade was> | <Honest grade> | <Reason> | <Criteria affected>

- Pass N Accuracy: was A, honest retrospective B+. Reason: pilot-run later found "polygenic vs. phylogenetic" word-mixup in student's reading guide that the summary didn't list. Affects: Accuracy, Cross-Deliverable Consistency.
```

This goes in the same `grading_scorecard.md` file. Do NOT silently re-issue the earlier grade as if no gap was found.

### Common inflation patterns

From the pilot run:
- **Inflation type 1:** Grading against the handoff summary rather than primary source.
- **Inflation type 2:** Declaring "unverifiable" after one tool failed instead of trying another.
- **Inflation type 3:** Stopping at text extraction when images held test-critical content.
- **Inflation type 4:** "All A's means we're done" — no, "all A- or above per target" means we're done.

### When to stop

Stop the grading loop when **all 6 criteria are at target OR above AND the most recent pass included primary-source verification through Level 3 (images).**

Do NOT stop early just because the composite is at target if you haven't verified against primary sources. That's how the pilot run shipped 3 incomplete versions before the user flagged image gaps.

### When to revise

Any criterion below target → revise the affected deliverables → re-grade. Cap at 4-5 passes; if still failing after Pass 5, escalate to the user — either scope is too broad, target is too high for the evidence, or the team needs swapping.

## Composition with agentloop

study-prep's grading reuses agentloop's grading machinery:
- Letter grades (A+ through F) per criterion
- Anti-inflation selector (forced-choice grade anchors)
- Midpoint review after Pass 2
- Stall detection: same criterion at same grade for 2 consecutive passes → agent adaptation

See `~/.claude/skills/agentloop/phases/grading.md` for the underlying protocol. Don't duplicate — invoke it.

## Distribution QC

The final QC step is distribution. A bundle that's technically perfect but sitting in a dev directory the parent can't find is not a delivered bundle.

```
DISTRIBUTION CHECKLIST

[ ] student_downloads/ folder exists with all expected files
[ ] PRIMARY: Live URL via GitHub Pages — verified HTTP 200, content MD5 matches local
    (this is the one the student taps on her phone — always do this if gh is available)
[ ] SECONDARY: Bundle copied to iCloud Drive (if available) — confirmed path
[ ] SECONDARY: Apple Mail composer opened with zip attached, parent's address pre-filled
[ ] Content parity verified: md5 of local HTML == md5 of iCloud HTML == curl-MD5 of live URL
```

Check which cloud mounts exist before suggesting:
```bash
ls ~/Library/Mobile\ Documents/com~apple~CloudDocs/ \
   ~/Dropbox \
   ~/Library/CloudStorage/ 2>/dev/null
gh auth status   # for the live URL path
```

### Live-URL QA script

After publishing to GitHub Pages, verify:

```bash
URL="https://<user>.github.io/<repo>/"

# 1. Responds with 200
curl -s -o /dev/null -w "%{http_code}\n" "$URL"

# 2. Content matches what we pushed
REMOTE_MD5=$(curl -s "$URL" | md5)
LOCAL_MD5=$(md5 -q student_downloads/00_START_HERE.html)
[ "$REMOTE_MD5" = "$LOCAL_MD5" ] && echo "✓ parity" || echo "✗ DRIFT"

# 3. Pass-N-specific content is present on the live URL
for term in <comma-separated list of Pass-N-specific terms>; do
  curl -s "$URL" | grep -qi "$term" && echo "✓ $term" || echo "✗ MISSING: $term"
done
```

### If you update content after first publishing

Do NOT create a new repo — `git push` to the existing one. Then re-run the content-parity check above. GitHub Pages typically redeploys in ~60 seconds.

## Final run completeness

```
[ ] QC report written, all items checked
[ ] Grading scorecard shows every pass + any retrospective downgrades
[ ] All 6 criteria at target or above on the final pass
[ ] Distribution verified (student can access without involving the parent)
[ ] Memory updated: save any subject-specific lessons (e.g., "this teacher tests exact slide figures")
```
