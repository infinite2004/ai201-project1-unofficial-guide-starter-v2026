# Setup progress — 2026-09-21

- Created `.venv` with Python 3.12.13 and installed `requirements.txt`.
- Created `.env` from `.env.example`; the Gemini key is still a placeholder.
- Read `RUNNING.md` without changing it.
- Selected the default `campus_life` corpus and listed the available corpora.
- Read `admin_housing_lottery.txt`, `admin_withdrawal_deadline.txt`,
  `dining_pellew_dining_hall.txt`, and `housing_morrow_house_laundry.txt`.
  These are short posts with useful facts concentrated in individual sentences.
- Downloaded and verified the local embedding model (384-dimensional vectors).
- `python test.py`: 8 passed, 1 failed (missing real API key), 1 skipped
  (model call). The local vector-store round trip passed.
- `python -m pip check`: no broken requirements.
- `python app.py index`: stored 88 chunks from 88 documents. Mean chunk
  length 317 characters, shortest 178, longest 549; `chunker.py::fallback_split`.
- `python app.py --corpus advice_threads chunks -n 1`: **26 chunks total**.
- Filled five questions and expected phrases in `questions.py` from the source
  documents before running any evaluation. No evaluation has been run.

## Still required

1. Enter your own `GEMINI_API_KEY` in `.env`, then run `python test.py` and
   `python app.py ask "is the housing lottery random?"` to verify generation.
2. The project is now connected to the existing history of
   `https://github.com/infinite2004/ai201-project1-unofficial-guide-starter-v2026`.
   Setup and question changes are being committed separately; the end-to-end
   milestone remains incomplete until a real model answer is verified.
3. Write your two original acceptance criteria and reasons for all five, as
   required by the instructions. `criteria.md` is unchanged pending your wording.
4. Pressure-test the completed criteria and commit/push the milestone work.

Activate the environment in each new terminal with `source .venv/bin/activate`.
