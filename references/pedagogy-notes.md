# Pedagogy Notes — Why Each Deliverable Exists

Everything in the deliverable set is backed by learning-science research. Understanding why helps Claude produce materials that actually work, not just materials that look thorough.

## Research-backed techniques used

### 1. Retrieval practice > re-reading
**Source:** Karpicke & Blunt 2011, Roediger & Butler 2011, and a large meta-analysis by Adesope et al. 2017.

Students who self-test retain ~50% more than students who re-read, measured at a delay of a week or more. The quiz bank and retrieval-practice prompts at the end of each study-guide section exist because of this. Not because we want the student to feel productive, but because retrieval is causally better for long-term retention.

**Implication for study-prep:** every content section ends with a "Check Yourself" prompt that forces the student to recall without looking. Never passive re-reading.

### 2. Refutation text (surfacing the wrong version)
**Source:** Guzzetti 1993, Tippett 2010.

When students hold a misconception, showing the misconception + correction side-by-side overwrites it more reliably than showing only the correct version. Merely stating the correct version lets the misconception persist.

**Implication for study-prep:** "Errors in My Notes" always shows the wrong version with strikethrough next to the correct version. The temptation to "just teach them the right version" is wrong for students who've already absorbed the wrong one.

### 3. Interleaving
**Source:** Rohrer & Pashler 2007, Birnbaum et al. 2013.

Mixing topics inside a study session ("do some Ch 17, some Ch 18, some Ch 19") produces better long-term retention than blocking ("do all Ch 17, then all Ch 18, then all Ch 19"). Interleaving feels harder in the moment, which is why students avoid it without instruction.

**Implication for study-prep:** the study plan explicitly instructs the student to mix chapters within a session, and explicitly warns them that it will feel harder.

### 4. Spaced retrieval
**Source:** Cepeda et al. 2006 meta-analysis.

Distributing study sessions across multiple days vastly outperforms cramming the same total time into one day. The optimal spacing depends on the retention interval, but for a 1-week horizon, 3 sessions beats 1 session of equal total time.

**Implication for study-prep:** the study plan is always multi-day. Even if the test is tomorrow, we plan tonight + tomorrow morning.

### 5. Error-first ordering
**Source:** interference theory, proactive/retroactive interference.

If a student reviews correct material and THEN sees their error card, the error can retroactively interfere with the correct material. Reverse order avoids this.

**Implication for study-prep:** "Errors in My Notes" is the FIRST tab in the nav, and the first step in the study plan.

### 6. Dual coding
**Source:** Mayer & Moreno 2003, Paivio 1971.

Pairing text with images produces better recall than text alone. Visual diagrams are not decorative — they're a second encoding channel.

**Implication for study-prep:** every major concept gets a visual. SVGs are inline in the study guide, not linked.

### 7. Elaborative interrogation (the "why")
**Source:** Willoughby et al. 1994.

Asking "why is this true?" or "why does this rule make sense?" produces better retention than memorizing the rule alone. This is why error cards include a `why:` field — not just "this is wrong, this is right" but "this is wrong, this is right, and here's why the distinction matters."

**Implication for study-prep:** every error, every misconception callout, and every quiz answer includes a why.

## What NOT to do (from pilot observation)

- **Don't create "find the typo" exercises as the main study activity.** Looking for errors trains proofreading, not concept mastery. Use errors as anchors for correction, not as a primary task.
- **Don't write a cheat sheet that's comprehensive.** The cheat sheet's role is 15 minutes on test morning. If it's comprehensive, the student tries to read it all and panics. Keep it visual-dense and selective.
- **Don't give the student a README longer than 1 screen.** They won't read it. Tell them what to double-click and stop.
- **Don't deliver materials that require a build step.** Every file must open on a phone with no install.

## Grade-level calibration

| Grade range | Target reading level | Max sentence length | Vocabulary |
|-------------|----------------------|---------------------|------------|
| 6-8 | 6th-grade | ~15 words | Define every term on first use |
| 9-10 | 8th-10th grade | ~20 words | Use content terms freely; define technical ones |
| 11-12 / AP | 10th-12th grade | ~25 words | Assume textbook vocabulary |
| College | Adult general | no cap | Domain vocabulary assumed |

Adjust body text accordingly. Never lecture up.

## Accessibility notes

- Color contrast: all red/green combinations should also use a shape or bold cue for colorblind students.
- Font: system sans-serif (user's OS), minimum 10pt in PDFs.
- SVG text uses `<text>` elements, not converted to paths — keeps them copyable and screen-reader-accessible.
- Diagrams always include a short text description or caption; don't rely on the visual alone to carry information.
