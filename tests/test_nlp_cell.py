"""Run the notebook's NLP processing cell offline with a fake provider."""
import json
from pathlib import Path
import unittest

NOTEBOOK = json.loads(
    (Path(__file__).resolve().parents[1] / "News Scraping.ipynb").read_text(encoding="utf-8")
)


def processing_cell():
    return next("".join(cell["source"]) for cell in NOTEBOOK["cells"]
                if cell["cell_type"] == "code"
                and "generate_response(question)" in "".join(cell["source"]))


class FakeFrame:
    def __init__(self, rows):
        self.rows = rows
        self.iloc = rows

    def __len__(self):
        return len(self.rows)


class FakeTime:
    @staticmethod
    def time():
        return 0.0

    @staticmethod
    def sleep(seconds):
        pass


class NlpCellTests(unittest.TestCase):
    def run_cell(self, rows):
        prompts = []

        def generate_response(prompt):
            prompts.append(prompt)
            return "answer"

        namespace = {"df": FakeFrame(rows), "generate_response": generate_response,
                     "time": FakeTime, "print": lambda *args, **kwargs: None}
        exec(processing_cell(), namespace)
        return namespace["answers"], prompts

    def test_missing_article_text_is_skipped_without_an_api_call(self):
        answers, prompts = self.run_cell([{"long-content": float("nan")},
                                          {"long-content": "  "},
                                          {"long-content": "Article text"}])
        self.assertEqual(answers, ["no content", "no content", "answer"])
        self.assertEqual(len(prompts), 1)
        self.assertTrue(prompts[0].endswith("Article text"))

    def test_provider_errors_keep_their_existing_label(self):
        def failing(prompt):
            raise RuntimeError("context length exceeded")

        namespace = {"df": FakeFrame([{"long-content": "Article text"}]),
                     "generate_response": failing, "time": FakeTime,
                     "print": lambda *args, **kwargs: None}
        exec(processing_cell(), namespace)
        self.assertEqual(namespace["answers"], ["long text"])


if __name__ == "__main__":
    unittest.main()
