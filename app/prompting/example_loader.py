"""
example_loader.py

Loads and manages NL-to-SQL few-shot examples
stored in JSON files.
"""

import json
from pathlib import Path
from typing import Any


EXAMPLES_DIR = Path(__file__).parent / "examples"


class ExampleLoader:
    """
    Loads few-shot NL-to-SQL examples from JSON files.
    """

    def load_file(
        self,
        filename: str
    ) -> list[dict[str, Any]]:
        """
        Load examples from a single JSON file.

        Empty JSON files are treated as having zero examples.
        """

        file_path = EXAMPLES_DIR / filename

        if not file_path.exists():

            raise FileNotFoundError(
                f"Example file not found: {file_path}"
            )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read().strip()

        # Empty file = no examples yet
        if not content:
            return []

        try:

            examples = json.loads(content)

        except json.JSONDecodeError as error:

            raise ValueError(
                f"Invalid JSON in {filename}: "
                f"line {error.lineno}, "
                f"column {error.colno}"
            ) from error

        if not isinstance(examples, list):

            raise ValueError(
                f"{filename} must contain a JSON list."
            )

        return examples

    def load_all(self) -> list[dict[str, Any]]:
        """
        Load examples from all JSON files.
        """

        all_examples = []

        for file_path in sorted(
            EXAMPLES_DIR.glob("*.json")
        ):

            examples = self.load_file(
                file_path.name
            )

            all_examples.extend(examples)

        return all_examples

    def get_by_category(
        self,
        category: str
    ) -> list[dict[str, Any]]:
        """
        Return examples belonging to a category.
        """

        examples = self.load_all()

        return [
            example
            for example in examples
            if example.get("category") == category
        ]

    def count_examples(self) -> int:
        """
        Return the total number of examples.
        """

        return len(self.load_all())


if __name__ == "__main__":

    loader = ExampleLoader()

    examples = loader.load_all()

    print("=" * 60)
    print("FEW-SHOT EXAMPLE BANK")
    print("=" * 60)

    print(
        f"Total examples: {len(examples)}"
    )

    print()

    for example in examples:

        print(
            f"{example['id']} | "
            f"{example['category']} | "
            f"{example['difficulty']}"
        )
    