# Milestone 2: options, ranked reasons, and review

AI-authored planning notes, prepared at the student's explicit request.
The assignment asks the student to author their criteria, so these notes do
not establish compliance with that authorship requirement.

## Criterion options

The first three criteria in `criteria.md` were provided by the assignment.
Choose a chunk criterion and a second criterion from these additional options:

| Option | Measurable target | Decision |
| --- | --- | --- |
| Chunk completeness | At least 4 of 5 printed chunks retain a complete fact, intact sentence/paragraph boundaries, and an explicit subject. | Selected as criterion 4 |
| Factual reliability | At least 4 of 5 questions get three correct, expected-phrase-matching answers with no unsupported factual claims. | Selected as criterion 5 |
| Chunk length | At least 4 of 5 printed chunks contain 150–600 characters. | Length alone does not establish meaning |
| Source validity | Every cited filename in 15 answers exists among that answer's retrieved sources. | Useful additional citation check |
| Numeric fidelity | Every price and time range stated in 15 answers exactly matches the retrieved source. | Useful but narrower than factual reliability |
| Concision | At least 12 of 15 substantive answers contain at most 100 words. | Secondary to correctness |
| Retrieval rank | The first returned chunk directly answers at least 4 of 5 questions. | Stricter alternative to criterion 1 |
| Response time | At least 4 of 5 sequential warm queries complete within 15 seconds, with no cache and including rate-limit waits. | Provider-dependent; lower priority |

## Fifteen reasons ranked by importance

This is a design judgment for this corpus, not a ranking derived from evaluation.
The top five supply the reasons in `criteria.md`.

1. **Correct facts — criterion 5.** Campus prices, wait times, and rules lose
   their usefulness if details change during generation. Require three correct
   answers per question for at least four questions to test consistency.
2. **Evidence availability — criterion 1.** Similar dorm and dining posts can
   compete in search. Four of five requires broad coverage while allowing one
   miss; fewer successes would leave too many ordinary questions unsupported.
3. **Unsupported-question refusal — criterion 3.** Campus documents cannot
   support unrelated topics. Four of five demands that most clear misses stop
   before generation while allowing one accidental semantic match.
4. **Preserved context — criterion 4.** A sentence about a price or schedule
   needs its subject. Four of five sampled chunks must preserve complete facts,
   boundaries, and a named subject to remain independently useful.
5. **Traceability — criterion 2.** Filenames already travel with the evidence,
   so every substantive answer should identify at least one. Multiple citations
   are unnecessary when one post answers the question.
6. **Numeric fidelity.** A wrong dollar amount or time range can change a
   student's decision even when the rest of an answer sounds plausible.
7. **Repeatability.** Three uncached answers reveal variation that a single
   successful response cannot show.
8. **Correct attribution.** An existing filename alone does not prove that its
   text supports the answer; checking claims against context is stronger.
9. **No misleading fragments.** Tiny tail chunks may contain words without an
   independently usable fact.
10. **Focused chunks.** Combining unrelated topics may weaken retrieval for a
    question that needs only one of them.
11. **Avoiding false refusals.** Refusing an answerable question makes useful
    source material inaccessible; criterion 5 counts this as failure.
12. **Reproducible sampling.** Saving the five chunks printed by the command
    keeps reviewers from silently selecting only favorable examples.
13. **Concise answers.** Direct fact questions benefit from short responses,
    but brevity cannot compensate for incorrect information.
14. **Latency.** Fast answers are helpful, but external rate limits and network
    variation make speed less central than evidence and accuracy here.
15. **Token efficiency.** Smaller contexts can reduce usage, but removing needed
    context to save tokens would undermine the main purpose of the system.

## Local measurability check

| Criterion | Sample and observation | Pass rule |
| --- | --- | --- |
| 1 | Five retrievals; inspect returned chunks for the requested fact and subject | At least four questions have an answering chunk |
| 2 | Fifteen generated outputs; inspect substantive answer text for a supplied filename | Every substantive answer cites at least one source |
| 3 | Five distinct out-of-scope questions; inspect gate decision and exact refusal | At least four gate refusals before generation |
| 4 | Five command-selected chunks; check complete sentence, source boundaries, explicit subject | At least four chunks pass all three checks |
| 5 | Three uncached outputs for each of five questions; inspect phrase, factual correctness, claim support | At least four questions pass on all three outputs |

Each criterion now specifies observable evidence and a pass rule. This is a
review of the test plans, not evidence that the system meets the targets.
No five-question evaluation or retrieval tuning was performed for this review.

The course's linked acceptance-criteria guide and criteria self-check could not
be retrieved through the browser tool. The local review above is not claimed
to be completion of that unavailable course self-check.

History: the environment check and housing-lottery smoke question ran before
these criteria were completed. The five-question evaluation has not run.
