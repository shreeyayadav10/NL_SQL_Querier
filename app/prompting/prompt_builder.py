"""
prompt_builder.py

Builds the complete prompt sent to the NL-to-SQL model.
"""

from typing import Any

from app.prompting.example_selector import ExampleSelector
from app.prompting.system_prompt import SYSTEM_PROMPT
from app.prompting.prompt_config import (
    MAX_FEW_SHOT_EXAMPLES
)


class PromptBuilder:
    """
    Builds prompts using:

    - system instructions
    - database schema
    - relevant few-shot examples
    - user question
    """

    def __init__(
        self,
        schema: str,
        max_examples: int = MAX_FEW_SHOT_EXAMPLES
    ) -> None:

        self.schema = schema

        self.example_selector = ExampleSelector(
            max_examples=max_examples
        )

    def _format_examples(
        self,
        examples: list[dict[str, Any]]
    ) -> str:
        """
        Format selected examples for the prompt.
        """

        if not examples:
            return "No few-shot examples available."

        formatted_examples = []

        for index, example in enumerate(
            examples,
            start=1
        ):

            formatted_examples.append(
                f"""
Example {index}

Question:
{example["question"]}

SQL:
{example["sql"]}
""".strip()
            )

        return "\n\n".join(
            formatted_examples
        )

    def build(
        self,
        question: str
    ) -> dict[str, str]:
        """
        Build the complete SQL-generation prompt.
        """

        selected_examples = (
            self.example_selector.select(
                question
            )
        )

        examples_text = self._format_examples(
            selected_examples
        )

        user_prompt = f"""
DATABASE SCHEMA
===============

{self.schema}


FEW-SHOT EXAMPLES
=================

{examples_text}


USER QUESTION
=============

{question}


TASK
====

Generate the SQLite SELECT query that answers
the user's question.

Return ONLY the SQL query.
""".strip()

        return {
            "system_prompt": SYSTEM_PROMPT.strip(),
            "user_prompt": user_prompt,
        }


if __name__ == "__main__":

    schema = """
TABLE: orders

COLUMNS:
- order_id: TEXT [PRIMARY KEY]
- customer_id: TEXT
- order_status: TEXT
- order_purchase_timestamp: TEXT

RELATIONSHIPS:
- customer_id → customers.customer_id


TABLE: customers

COLUMNS:
- customer_id: TEXT [PRIMARY KEY]
- customer_state: TEXT
"""

    builder = PromptBuilder(
        schema=schema
    )

    question = (
        "How many orders were placed in 2018?"
    )

    prompt = builder.build(
        question
    )

    print("=" * 70)
    print("PROMPT BUILDER TEST")
    print("=" * 70)

    print("\nSYSTEM PROMPT")
    print("-" * 70)

    print(prompt["system_prompt"])

    print("\nUSER PROMPT")
    print("-" * 70)

    print(prompt["user_prompt"])