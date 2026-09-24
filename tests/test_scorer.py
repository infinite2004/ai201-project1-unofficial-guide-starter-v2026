import unittest

import questions
from run_eval import load_scorer
from scorer import judge


class ScorerTests(unittest.TestCase):
    def test_runner_discovers_scorer_and_five_populated_questions(self):
        self.assertIs(load_scorer(), judge)
        self.assertEqual(len(questions.answered()), 5)
        self.assertTrue(all(q.get("expects", "").strip() for q in questions.answered()))

    def test_missing_fact_and_empty_expectation_fail(self):
        self.assertFalse(judge("Price?", "$1.50", "It costs $1.75.", []))
        self.assertFalse(judge("Price?", "  ", "Anything", []))

    def test_case_and_whitespace_follow_existing_criterion(self):
        self.assertTrue(judge("When?", "Tuesday or Wednesday",
                              "TUESDAY  or\nWednesday morning.", []))

    def test_documents_do_not_substitute_for_answer(self):
        self.assertFalse(judge("Price?", "$1.50", "I don't know.",
                               [{"text": "It costs $1.50."}]))

    def test_known_substring_limits_are_explicit(self):
        # False positive: added unsupported claim. Manual grounding must fail it.
        self.assertTrue(judge("Price?", "$1.50",
                              "$1.50. Every student gets free detergent.", []))
        # False negative for semantic correctness: equivalent numeric range.
        self.assertFalse(judge("Wait?", "12 to 18 minutes",
                               "12–18 minutes.", []))


if __name__ == "__main__":
    unittest.main()
