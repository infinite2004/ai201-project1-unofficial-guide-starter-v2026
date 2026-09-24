# Slides 13–29: actions, changes, and attention items

Source: `AI201 L2 · Fa26 S3.pdf`, numbered slides 13–29 (same PDF page numbers).
Reviewed text and rendered images of all 17 slides on September 23, 2026.
The user's request authorizes applicable project work. Classroom prompts in the
slides are treated as exercises; no class-chat message, peer participation, or
submission is claimed.

## Slide-by-slide record

| Slide | Request or lesson | Action/result |
|---|---|---|
| 13 | Separate retrieval failure from generation failure | Captured full retrieved chunks for all 15 answers. Reviewed both stages independently: all five questions retrieve the correct fact and all 15 answers use it correctly. |
| 14 | More retrieval must earn its value | Retained top-k 4; no evidence in this run justifies retrieving more. Some lower-ranked hits are unrelated, but the correct answer is rank one for all five questions. No comparative improvement is claimed. |
| 15 | Brainstorm campus questions | Drafted examples below, including an additional two-fact challenge. These are Codex drafts, not a report of classroom discussion. |
| 16 | Classify whether two scorers could agree | Classified drafts below; checked all five existing questions against the actual campus documents. Each asks a specific supported fact. No independent two-person agreement study was performed. |
| 17 | Convert untestable prompts into document-grounded questions | Rewrote dining, lottery, and parking examples below with named facts and source documents. |
| 18 | Write a challenging testable question | Added CHALLENGE_QUESTIONS with a two-fact Pellew question and predeclared facts. Kept it separate from the original five-question baseline; no challenge result is claimed. |
| 19 | Inspect supplied evaluation runner | Confirmed it loads questions, discovers scorer.judge, makes three uncached calls per question, and writes reports. |
| 20 | Create scorer.py with exact interface | Implemented judge(question, expects, answer, results) -> bool. Runner discovery and execution verified. |
| 21 | Load five questions; fill expects before observing results | Verified exactly five populated questions and five nonempty expectations before the live run. Existing expectations were preserved. Class-chat check-in is for the student. |
| 22 | Expected-phrase scoring; pass/fail and total | Added case/whitespace-normalized substring check and per-run totals. Phrase presence in retrieved text alone cannot pass an answer. |
| 23 | Run three times | Completed 15 uncached Gemini calls: phrase totals 5/5, 5/5, 5/5. Recorded actual answers and context in paired Markdown/JSON reports. |
| 24 | Identify stable and variable measurements | Verified each question's retrieval results and distances are identical in all three runs. Generated wording varied, but the measured scores did not. Gate and chunk inspection are one deterministic measurement each. |
| 25 | Aggregate questions into criteria; paste real text | Filled README's five-row Before run log, with real retrieval, answer, gate, and chunk output and file/function provenance. |
| 26 | Apply targets across all runs | Recorded five MET verdicts under the unchanged criteria. Explained that 4/5, 3/5, 4/5 would miss a 4/5 target, and criterion 5 requires the same questions to pass all three runs. |
| 27 | Explain substring limitations and review manually | Read all 15 answers against their captured chunks. Added tests showing unsupported extra claims can pass and equivalent numeric formatting can fail. AI review is explicitly disclosed. |
| 28 | Preserve original criteria if revising | No revision was necessary. criteria.md remains byte-for-byte unchanged. README explains the append-only revision rule. |
| 29 | Distinguish measurement flaw from missed result | Documented scorer limitations without retroactively changing targets. No target was lowered and no result was relabeled to improve the score. |

## Discussion exercise: drafts, classification, and rewrites

| Rough prompt | Testable as written? Why? | Document-grounded rewrite and answer |
|---|---|---|
| What are good dining halls? | No: “good” has no shared scoring rule. | What are the peak wait times at Pellew Dining Hall? 12 to 18 minutes, dining_pellew_dining_hall.txt. |
| Is the housing lottery fair? | No: fairness is an opinion without an agreed definition. | What determines junior/senior priority before random tie-breaking? Accumulated credit hours, admin_housing_lottery.txt. |
| Tell me about parking. | No: open-ended request without a specific correctness target. | Does the corpus say there is a parking-permit waitlist? No waitlist, admin_parking_permits.txt. |
| How much is a wash in Morrow House? | Yes: a named service and price exist in the documents. | $1.50 per wash, housing_morrow_house_laundry.txt. |
| Who will win next year's housing lottery? | No: future winners are not in these documents; this belongs in refusal testing. | How are rising sophomores assigned lottery numbers? Random draw, admin_housing_lottery.txt. |
| When is Pellew's peak period, and what is the cash price? | Yes: two explicit facts; stronger test of completeness and correct subject. | 11:45 to 12:30 and $11.75, dining_pellew_dining_hall.txt. Added as an unrun challenge. |

The original five questions cover lottery credit hours, adviser signature,
Pellew wait duration, Morrow wash price, and Morrow laundry mornings. Their
supporting passages and all-answer review are in README's Unit 2 section.

## Files changed

- `scorer.py`: new expected-phrase scorer with the required interface and limitations.
- `run_eval.py`: prints per-run totals; reports model/chunk settings; saves full
  retrieval/answers/scores as JSON alongside Markdown; uses precise timestamps
  to avoid overwriting evidence from two evaluations within the same minute.
- `questions.py`: separate, predeclared challenge list; original five questions,
  expectations, out-of-scope questions, and answered() behavior unchanged.
- `tests/test_scorer.py`: five tests covering runner discovery, populated inputs,
  missing facts, normalization, answer-vs-retrieval separation, and known limits.
- `README.md`: filled Unit 2 Before run log and verdicts, source-backed review,
  actual output, stability findings, scorer limitations, and revision decision.
- `results/run_2026-09-23_203653_702014_before.md` and `.json`: live evaluation evidence.
- `results/unit-2-chunks.txt`: freshly captured five-chunk sample.
- This file: slide coverage, discussion drafts, change list, and student actions.

Local tooling: installed PyMuPDF 1.28.2 in the existing .venv to read/render the
PDF. This is a review dependency; application requirements were not changed.
The first sandboxed eval stopped before generation because ONNX could not create
its working directory. The authorized unrestricted rerun completed successfully.

## Verification

- `python -m unittest discover -s tests -v`: 9 tests passed (4 existing, 5 new).
- Actual live evaluation: 15 calls, caching disabled; 7,730 reported tokens.
- Expected phrase: 15/15; retrieved filename in answer: 15/15.
- Correct subject/fact retrieval: 5/5 each run; all 15 factual reviews pass.
- Gate: 5/5 rejected at 0.69. Existing Unit 1 pipeline evidence additionally
  checks the exact refusal string and zero generation calls at this cutoff.
- All five freshly printed sample chunks pass the three original chunk checks.

## Needs the student's attention

1. Read and understand scorer.py. Slides 19–22 make the scoring decision part of
   the learning exercise. Codex wrote this implementation; do not describe it as
   independently student-written. The README records that authorship.
2. Independently review the run-log verdicts, especially factual support. The
   substring scorer cannot certify those judgments, and Codex's review is not
   a second human scorer's agreement.
3. The original five questions were already used for tuning. Review the drafted
   challenge and add your own difficult supported questions before treating the
   perfect baseline score as evidence of broader reliability.
4. If class participation is still required, post your own “five questions loaded”
   check-in and the 5/5, 5/5, 5/5 phrase totals. No class-chat message was sent.
5. The later improvement/after-run/reflection sections remain pending because
   they are beyond slides 13–29. No before/after improvement is claimed.
6. Existing Unit 1 attention items still apply: AI-drafted criteria, course
   self-check, and portal submission were already disclosed as needing review.
   This task did not submit, commit, or push anything.
