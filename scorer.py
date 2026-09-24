"""AI-assisted slide 20–22 exercise: expected-phrase check only.

A pass does not prove correctness, source attribution, or factual grounding.
Those checks remain separate in the criterion review.
"""


def normalize(text: str) -> str:
    """Ignore case and repeated whitespace, as criterion 5 specifies."""
    return " ".join(text.casefold().split())


def judge(question, expects, answer, results) -> bool:
    """Return whether the nonempty expected phrase occurs in the answer.

    question and results are retained for the run_eval.py interface. We do
    not count a phrase found only in a retrieved chunk as an answer pass.
    """
    phrase = normalize(expects)
    return bool(phrase) and phrase in normalize(answer)
