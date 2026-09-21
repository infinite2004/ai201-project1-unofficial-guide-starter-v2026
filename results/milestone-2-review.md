# Milestone 2 review

This review was written by Codex at the student's request. It records a technical
assessment, not a claim about the student's personal preferences or independent
authorship. No retrieval or generation evaluation was run for this review.

## Criterion 4: Is the chunk target appropriate?

Yes. For this corpus, a useful chunk must preserve a complete fact and identify
what that fact describes. For example, "$1.50 wash" is less useful if the chunk
loses the information that it describes Morrow House. Sentence boundaries help
keep qualifications attached to the facts they qualify.

The target requires four of five samples to satisfy all three checks, allowing
one failure without accepting widespread fragmentation. It is a small-sample
check, not proof that every chunk in the corpus works. The starter already keeps
these short posts whole, so the target also protects against regressions when
Milestone 3 introduces a new chunker. A passing score alone would not prove the
new chunker is better than the starter.

## Criterion 5: Is the accuracy target appropriate?

Yes, as a demanding reliability target. Four questions must each succeed on all
three uncached attempts. Twelve successes scattered across fifteen outputs do
not necessarily pass: the successes must cover all three attempts for at least
four questions. A refusal on an answerable question fails that attempt.

Each answer must supply the requested fact and support every factual claim with
the retrieved context. This checks whether the system preserves prices, times,
and policy details instead of merely sounding confident.

The existing expected-phrase requirement is stricter than semantic correctness:
"12–18 minutes" could express the correct fact but fail a literal match for
"12 to 18 minutes." Keep that limitation visible when interpreting results;
do not silently count paraphrases as literal matches or change the original
target after seeing a failure. The factual check and phrase check are distinct.

## The five reasons in plain language

These are the design reasons supporting the targets; they are not attributed
as personal statements by the student.

1. **Retrieval:** Several posts describe similar campus locations. Requiring
   four correct retrievals allows one mix-up but still requires the system to
   find evidence for most questions. Requiring only three would leave too many
   questions unsupported; requiring five would allow no miss.
2. **Sources:** Each answer should let the reader find its evidence. The
   pipeline already has filenames, so every substantive answer should name one.
   One is enough when a single post contains the answer.
3. **Refusals:** Campus documents cannot answer questions from unrelated
   subjects. Rejecting four of five unrelated questions allows one accidental
   match, but rejecting only three would permit too many unsupported requests.
4. **Chunks:** A fact needs enough surrounding text to identify its subject.
   Four of five complete, independently understandable chunks allows one awkward
   split while requiring most samples to preserve meaning. Character count
   alone would not establish that.
5. **Accuracy:** A wrong price, wait time, or rule can make an answer useless.
   Three successful attempts for four questions checks consistency and allows
   one difficult question; one successful attempt could just be a lucky output.

## How someone would test each criterion

| Criterion | Procedure | Passing result |
| --- | --- | --- |
| 1: Retrieval | Retrieve once for each of the five questions with recorded settings. Read the returned chunks and check for the actual answer about the correct subject. | At least four questions have an answering chunk. |
| 2: Sources | Generate three uncached outputs for each question. Inspect the substantive answer text for a filename supplied in its retrieved context. The separate source list does not count. | Every substantive answer names at least one source. Gate refusals are assessed separately. |
| 3: Refusals | Try each of the five distinct `OUT_OF_SCOPE` questions once. Check that the gate rejects before generation and returns the exact refusal constant. | At least four of five are refused by the gate. |
| 4: Chunks | Save the five chunks from `python app.py chunks -n 5`. Compare each with its original source for a complete factual sentence, intact boundaries, and an explicit subject in the chunk text. | At least four chunks satisfy all three checks. |
| 5: Accuracy | Inspect the fifteen uncached outputs for the correct fact, expected phrase, and support for every factual claim in the retrieved context. Count in-scope refusals as failures. | At least four questions pass on all three attempts. |

Record the corpus, chunker, top-k, and threshold with the evidence. These
procedures describe future checks; no passing evaluation score is claimed here.

## Are the five questions suitable?

Yes. All five ask for specific facts explicitly present in the chosen corpus.
The table below checks them against source documents, not model outputs.

| Question | Expected phrase | Source and factual answer |
| --- | --- | --- |
| What determines housing lottery priority for juniors and seniors before random tie-breaking? | `credit hours` | `admin_housing_lottery.txt`: accumulated credit hours determine priority before random ties. |
| What signature is required to withdraw from a course? | `adviser` | `admin_withdrawal_deadline.txt`: withdrawal requires an adviser signature. |
| What are the peak wait times at Pellew Dining Hall? | `12 to 18 minutes` | `dining_pellew_dining_hall.txt`: peak waits are 12 to 18 minutes. |
| How much does one wash cost in Morrow House's laundry room? | `$1.50` | `housing_morrow_house_laundry.txt`: a wash costs $1.50. |
| Which mornings are best for doing laundry in Morrow House? | `Tuesday or Wednesday` | `housing_morrow_house_laundry.txt`: Tuesday or Wednesday morning is best. |

The questions cover policy, dining, and housing and include a numeric price,
a time range, and named days. Two use the same laundry document, so the set
covers four documents rather than representing all 88. It is suitable for the
required small test set, but success would not establish corpus-wide accuracy.

## Completion status

- Five populated questions, each with an expected phrase: complete.
- Five numbered criteria, each with a target and reason: complete.
- A clear test procedure for each criterion: complete.
- Criterion options, 15 ranked reasons, and the selected top five: complete.
- Local review of clarity and source support: complete.
- Five-question evaluation: intentionally not run yet.

The repository's Milestone 2 documents are complete. The assignment's separate
student-authorship requirement cannot be satisfied by this AI-written review.
The linked course self-check was inaccessible to the browser tool; this local
review is not represented as completion of that course activity.
