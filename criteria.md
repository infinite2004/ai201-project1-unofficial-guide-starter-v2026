# Acceptance criteria — The Unofficial Guide

These targets cover the `campus_life` corpus. They were completed before
Milestone 3 changes, Milestone 4 tuning, or evaluation of the five test questions.
The starter setup and one housing-lottery smoke question had already run.

**Authorship:** Codex drafted and selected these criteria and reasons at the
student's request. They are not represented as independently student-written.
The assignment asks for student-authored criteria; student review and ownership
of these choices remain necessary before submission.

## Test scope

Use the five entries in `QUESTIONS` and five entries in `OUT_OF_SCOPE` in
`questions.py`. Record the corpus, chunker, top-k, and threshold with each run.
For generation criteria, use three uncached answers per in-scope question
(15 outputs). These are targets and test plans, not measured results.

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:** The questions ask for specific facts, but the corpus has
similar posts about different dorms and dining halls that can compete in search.
Four of five permits one such retrieval miss; a lower target would leave too
many everyday questions without evidence, while five of five allows no miss.

**How to test:** Retrieve once for each question using the recorded top-k.
Count a question as passing only when at least one returned chunk directly
states its answer about the correct location or policy. Require at least four
passes; the `expects` phrase is a clue, not sufficient proof by itself.

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:** The pipeline already supplies source filenames, so every
substantive answer should make its evidence traceable. Allowing even one
uncited answer would remove that check for a user; requiring multiple sources
would be unnecessary when one short post contains the whole answer.

**How to test:** For each of the 15 outputs, check that the answer text itself
names at least one filename supplied in its retrieved context. A separate
retrieved-sources list does not count. All substantive answers must pass.
A gate refusal is not a substantive answer and is assessed under criterion 3;
it still counts as a failure under criterion 5 for an in-scope question.

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:** These documents cover campus life, so unrelated questions
should usually stop before generation. Four of five permits one accidental
semantic match while demanding rejection of most unsupported questions; five
of five would allow none, and three of five would tolerate two unsupported calls.

**How to test:** Run each of the five distinct `OUT_OF_SCOPE` questions once
with the recorded threshold. Count a pass only when the gate rejects the
question before generation and returns `gate.REFUSAL` exactly (including its
final period). Require at least four passes; repeating one question five times
does not supply five distinct cases.

## 4. Chunks retain complete facts and their subject

At least 4 of the 5 chunks printed by `python app.py chunks -n 5` must contain
at least one complete factual sentence, begin and end at a sentence or paragraph
boundary in the source, and identify the relevant place, course, or policy in
the chunk text without requiring a neighboring chunk.

**Why this target:** Campus posts often put an actionable fact in one sentence
and its subject in a title. Requiring both protects meaning when posts are split;
four of five allows one awkward boundary, while a length-only target could reward
fragments and a perfect score would allow no exception in the sample.

**How to test:** Save the five printed chunks with their sources and function
name. For each, compare its boundaries with the source and mark all three checks:
complete factual sentence, intact boundaries, and explicit subject in the text.
A chunk passes only if all three checks pass. Require four passing chunks.

## 5. Answers preserve the requested fact without unsupported claims

For at least 4 of the 5 in-scope questions, all three uncached answers must state
the correct requested fact, include the question's `expects` phrase (ignoring
case and repeated whitespace), and contain no factual claim unsupported by the
retrieved chunks. An in-scope refusal counts as a failure.

**Why this target:** Laundry prices, dining wait times, and administrative rules
must retain their details to be useful. Requiring three consistent answers for
four questions checks reliability while allowing one difficult question; accepting
one lucky answer would hide variation, while five of five would permit none.

**How to test:** Compare each of the 15 answers with its question and retrieved
context. Check the expected phrase, the correctness of the requested fact, and
support for every factual claim. A question passes only if all three answers
pass every check. Require at least four passing questions.

---

Missing a target is a result to diagnose, not a reason to lower it. Preserve
these originals when documenting any later clarification.

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
