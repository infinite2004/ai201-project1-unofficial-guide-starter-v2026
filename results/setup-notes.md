# Setup progress — 2026-09-21

- Created `.venv` with Python 3.12.13 and installed `requirements.txt`.
- Created `.env` from `.env.example`; the locally saved Gemini key was verified.
- Read `RUNNING.md` without changing it.
- Selected the default `campus_life` corpus and listed the available corpora.
- Read `admin_housing_lottery.txt`, `admin_withdrawal_deadline.txt`,
  `dining_pellew_dining_hall.txt`, and `housing_morrow_house_laundry.txt`.
  These are short posts with useful facts concentrated in individual sentences.
- Downloaded and verified the local embedding model (384-dimensional vectors).
- `python test.py`: 10 passed, 0 failed, 0 skipped, including a real Gemini
  response and the local vector-store round trip.
- `python -m pip check`: no broken requirements.
- `python app.py index`: stored 88 chunks from 88 documents. Mean chunk
  length 317 characters, shortest 178, longest 549; `chunker.py::fallback_split`.
- `python app.py --corpus advice_threads chunks -n 1`: **26 chunks total**.
- Filled five questions and expected phrases in `questions.py` from the source
  documents before running any evaluation. No evaluation has been run.
- `python app.py ask "is the housing lottery random?"`: succeeded end to end.
  Best retrieval distance was 0.254 against a cutoff of 0.6. The answer explained
  that rising sophomores receive random numbers, whereas juniors and seniors
  are ordered by accumulated credit hours before random tie-breaking. It cited
  `admin_housing_lottery.txt`. One model call used 668 tokens.
- Setup notes and test questions were committed and pushed to
  `https://github.com/infinite2004/ai201-project1-unofficial-guide-starter-v2026`.

## Still required

1. Write your two original acceptance criteria and reasons for all five, as
   required by the instructions. `criteria.md` is unchanged pending your wording.
2. Pressure-test the completed criteria and commit/push the milestone work.

Activate the environment in each new terminal with `source .venv/bin/activate`.
