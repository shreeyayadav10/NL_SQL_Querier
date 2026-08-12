"""
example_selector.py

Selects the most relevant few-shot examples
for a user's natural-language question.
"""

import re
from typing import Any

from app.prompting.example_loader import ExampleLoader


class ExampleSelector:
    """
    Selects relevant few-shot examples using
    lightweight keyword and concept matching.
    """

    def __init__(
        self,
        max_examples: int = 5
    ) -> None:

        self.max_examples = max_examples
        self.loader = ExampleLoader()

        self.examples = self.loader.load_all()

    def _tokenize(
        self,
        text: str
    ) -> set[str]:
        """
        Convert text into lowercase tokens.
        """

        words = re.findall(
            r"[a-zA-Z_]+",
            text.lower()
        )

        return set(words)

    def _score_example(
        self,
        question: str,
        example: dict[str, Any]
    ) -> int:
        """
        Calculate a relevance score for one example.
        """

        question_tokens = self._tokenize(
            question
        )

        example_question_tokens = self._tokenize(
            example["question"]
        )

        concept_tokens = set()

        for concept in example.get(
            "concepts",
            []
        ):

            concept_tokens.update(
                self._tokenize(concept)
            )

        score = 0

        # Direct question-word overlap
        score += len(
            question_tokens
            & example_question_tokens
        ) * 3

        # SQL concept overlap
        score += len(
            question_tokens
            & concept_tokens
        ) * 2

        # Category-related keywords
        category = example.get(
            "category",
            ""
        ).lower()

        category_keywords = {
            "sales": {
                "sales",
                "revenue",
                "order",
                "orders",
                "price",
                "freight"
            },
            "customer": {
                "customer",
                "customers",
                "state",
                "spent"
            },
            "product": {
                "product",
                "products",
                "category",
                "categories"
            },
            "seller": {
                "seller",
                "sellers"
            },
            "review": {
                "review",
                "reviews",
                "rating",
                "score"
            },
            "time": {
                "year",
                "month",
                "date",
                "time",
                "daily",
                "monthly",
                "yearly",
                "delivery"
            }
        }

        relevant_words = category_keywords.get(
            category,
            set()
        )

        score += len(
            question_tokens
            & relevant_words
        )

        return score

    def select(
        self,
        question: str
    ) -> list[dict[str, Any]]:
        """
        Select the most relevant examples.
        """

        scored_examples = []

        for example in self.examples:

            score = self._score_example(
                question,
                example
            )

            scored_examples.append(
                (score, example)
            )

        scored_examples.sort(
            key=lambda item: item[0],
            reverse=True
        )

        selected = []

        for score, example in scored_examples:

            if score <= 0:
                continue

            selected.append(example)

            if len(selected) >= self.max_examples:
                break

        return selected


if __name__ == "__main__":

    selector = ExampleSelector(
        max_examples=5
    )

    test_questions = [
        "What are the top 10 product categories by revenue?",
        "What is the average review score for each customer state?",
        "Which sellers generated the highest revenue?",
        "How many orders were placed in 2018?"
    ]

    print("=" * 70)
    print("FEW-SHOT EXAMPLE SELECTOR")
    print("=" * 70)

    for question in test_questions:

        print()
        print(f"Question: {question}")
        print("-" * 70)

        selected_examples = selector.select(
            question
        )

        for example in selected_examples:

            print(
                f"{example['id']} | "
                f"{example['category']} | "
                f"{example['question']}"
            )