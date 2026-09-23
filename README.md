# The Unofficial Guide

Author: infinite2004 · Corpus: `campus_life`

Project: https://github.com/infinite2004/ai201-project1-unofficial-guide-starter-v2026

# Unit 1

## What This Does

The Unofficial Guide answers questions using 88 short campus-life documents.
It covers housing, dining, courses, and university procedures, including laundry
prices, dining wait times, and withdrawal requirements. It retrieves relevant
excerpts locally and asks Gemini to write a brief answer naming its source.
A relevance gate refuses questions when no excerpt is close enough; these are
fictional course documents, not official guidance for a real university.

## Chunking Strategy

**Chunk size:** 400-character soft target, including the title.
**Overlap:** 0 body characters; repeat the original title in every split chunk.
**Function:** `chunker.py::split_documents`.

The starter's 800-character windows with 120-character overlap produced 88 chunks
from 88 posts: average 317 characters, shortest 178, longest 549. It never split
a post. I kept short posts whole and changed longer ones to split at paragraph
boundaries, or sentence boundaries when a paragraph exceeds the target. Titles
travel with every chunk so a price or schedule still identifies its subject.
An oversized single sentence stays intact rather than being cut to fit.

The target sits above the original mean but below the longest posts, allowing
separate paragraphs in longer posts to come apart. No body overlap is needed
for these short facts; repeated sentences could crowd the search results.
The implementation produced 100 chunks: mean 282 characters, shortest 116,
longest 400. A short complete fact is acceptable; size alone is not quality.
The original `fallback_split` is retained for comparison. The lightweight English
sentence rule is not a general-purpose parser for every abbreviation.

The decision was recorded before implementation in
[the chunking plan](results/milestone-3-plan.md). Four regression tests passed,
including preservation of all campus body text without duplication, decimal
prices, empty input, and an oversized sentence. This does not establish a
retrieval improvement over the baseline.

## Sample Chunks

These are the five samples printed by `python app.py chunks -n 5`.

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```text
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_cs_210.txt#0` — produced by: `chunker.py::split_documents`

```text
CS 210 Data Structures

I'm a junior and I've done this twice now. Format is lecture with weekly labs; slides go up after class, not before. Assessment: two midterms and a final, all drawn from lecture material rather than the textbook. Midterms are curved, the final is not.

Expect 8 to 10 hours a week outside class.
```

**Chunk 3** — source: `course_math_220_workload.txt#0` — produced by: `chunker.py::split_documents`

```text
Workload for MATH 220 Linear Algebra

People keep asking so: 6 to 8 hours a week, almost all of it on problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_the_ridgeway_cafe_followup.txt#0` — produced by: `chunker.py::split_documents`

```text
Re: The Ridgeway Café

Adding to what people have said about The Ridgeway Café. The wait figure of 10 to 15 minutes at 12:30 matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: seating is tight; about 40 seats for a building of 900. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_morrow_house.txt#0` — produced by: `chunker.py::split_documents`

```text
Morrow House — what it's actually like

Just finished a year in this building. Built 1954, partially renovated 2008. Rooms are singles and doubles, hall bathrooms.

The good: cheapest housing tier by about $900 a year, and the singles are real singles.

The bad: known damp problem on the ground floor; two rooms were taken offline in 2024.
```

All five identify their subject, contain complete factual sentences, and start
and end at sentence or paragraph boundaries. Read independently, the first three
can answer: “When can I add a course?”, “Are CS 210 finals curved?”, and “How many
hours per week does MATH 220 take?” The fourth states when to avoid a café queue;
the fifth describes Morrow House's room types and damp problem. Each can answer
at least one concrete question without another chunk. This is an AI review of
the printed samples, not feedback from a breakout group.

## Sample Answer

**Question:** What are the peak wait times at Pellew Dining Hall?

**Answer (complete captured output, including source lines):**

```text
At Pellew Dining Hall, the peak wait times are 12 to 18 minutes.

Source: `dining_pellew_dining_hall.txt` (also mentioned in `dining_pellew_dining_hall_followup.txt`).

Sources retrieved: dining_halden_hall_followup.txt, dining_pellew_dining_hall.txt, dining_pellew_dining_hall_followup.txt, dining_the_ridgeway_cafe_followup.txt
```

**My relevance cutoff:** `0.69` (cosine distance; lower is closer).
**Top-k:** `4`.

| Question | In corpus? | Best distance |
|---|---|---|
| What determines housing lottery priority for juniors and seniors before random tie-breaking? | Yes | 0.208684 |
| What signature is required to withdraw from a course? | Yes | 0.558321 |
| What are the peak wait times at Pellew Dining Hall? | Yes | 0.197579 |
| How much does one wash cost in Morrow House's laundry room? | Yes | 0.195130 |
| Which mornings are best for doing laundry in Morrow House? | Yes | 0.283633 |
| What is the capital of Mongolia? | No | 0.824593 |
| How do I change the oil in a diesel engine? | No | 0.923117 |
| Who won the 1994 World Cup? | No | 0.885860 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.844232 |
| How do I write a for loop in Rust? | No | 0.890692 |

The highest in-corpus distance was 0.558321; the lowest out-of-corpus distance
was 0.824593. Their midpoint is about 0.691457, so I chose 0.69. All five
covered questions pass and all five unrelated questions are refused at this
cutoff. A cutoff of 0.3 would wrongly refuse the withdrawal question; a cutoff
of 0.9 would admit four of these unrelated questions. This is calibration on
ten known questions, not a guarantee for unseen questions near the boundary.

I first inspected five results per question. All five answer-bearing chunks
were already ranked first. The first three queries retrieved the housing
lottery policy, withdrawal policy, and Pellew wait-time post respectively;
these directly answered the questions rather than merely sharing words.
Lower ranks included distracting material: statistics exams for the lottery
question, unrelated course assessment for withdrawal, and other dining halls
for the Pellew question. Reducing top-k from 5 to 4 removed the last result
while retaining some supporting context. Other locations still appear in
context, so the model must respect the named subject; the gate checks only
the best distance, not the relevance of every returned chunk.

I inspected `GROUNDING_INSTRUCTION` in `generate.py` and the exact prompt printed
by `--show-prompt`. It already requires source-only information, refusal when
unsupported, a filename, and brevity. The sample preserved Pellew's 12–18-minute
range rather than borrowing a different hall's time, so I retained the instruction.
One successful answer does not establish the three-run accuracy criterion.

**Off-topic check:**

```text
Question: What is the capital of Mongolia?
I don't have enough information about that.
```

All five `OUT_OF_SCOPE` questions were also checked through the actual retrieval
and gate pipeline with generation replaced by a function that raises if called.
They all returned the exact refusal; generation was called zero times. A separate
CLI run confirmed the displayed refusal and zero model calls.

Evidence: [all retrieved chunks and distances](results/milestone-4-retrieval.md),
[machine-readable measurements](results/milestone-4-retrieval.json),
[initial top-5 exploration](results/milestone-4-top5-exploration.json),
[complete prompt and live answer](results/milestone-4-sample-answer.txt), and
[gate outcomes](results/milestone-4-refusals.json).

## How I Used AI

**1. Turning the chunking milestone into working code.** I asked Codex to finish
Milestones 3–5. It inspected the starter's 88-document/88-chunk baseline, recorded
a 400-character soft target with zero body overlap before coding, and implemented
paragraph/sentence splitting with the original title repeated. The resulting
change was from generic fixed windows to `chunker.py::split_documents`; Codex
also added tests for lost text, decimal prices, and oversized sentences and
pasted five actual samples into this README. I delegated those decisions and
edits rather than independently writing or manually correcting the function.
The original fallback remains available, and no retrieval improvement over the
baseline is claimed without a controlled comparison.

**2. Turning retrieval observations into a documented cutoff.** In the same
request, I asked Codex to complete retrieval tuning and the write-up. It returned
all ten measured best distances, full retrieved chunks, and a sourced Gemini
answer. It changed the starter's cutoff from 0.6 to 0.69 and top-k from 5 to 4
based on those observations, then verified five refusals without generation.
I used the AI-produced implementation and evidence; I did not manually revise
its measurements or conduct an independent breakout review. Codex retained the
existing grounding instruction because the inspected sample stayed within its
sources, and documented that one successful answer does not prove consistency.

Codex also drafted the Milestone 2 criteria at my request. Their AI authorship
is disclosed in `criteria.md`; this is not a claim that the course's requirement
for independently student-authored criteria has been satisfied. Likewise, the
linked course self-check was not accessible and has not been marked complete.

**Verification:** Four chunker regression tests passed. The supplied pipeline
smoke test passed for all four corpora using fake embeddings and fake generation
in a temporary vector store, keeping those checks separate from the live index.
The distances and sample answer above used the real embedding model and Gemini.
The full three-run Unit 2 evaluation has not been run.

**Run locally:** Use Python 3.11–3.13. Create `.venv`, install `requirements.txt`,
and copy `.env.example` to `.env` with your own key. Then activate the environment
and run `python app.py index` followed by `python app.py ask "your question"`.
See [RUNNING.md](RUNNING.md) for all commands. Secrets and local indexes are
excluded from Git.

**Submission URL:** https://github.com/infinite2004/ai201-project1-unofficial-guide-starter-v2026

The Unit 1 repository work is ready for review. The Course Portal submission
has **not** been made: browser access was denied in this session. Submit the URL
above through the course's project submission page. Keep this same repository
for Unit 2 so its history remains available.

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
