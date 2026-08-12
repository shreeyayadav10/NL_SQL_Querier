"""
sql_generator.py

Handles communication with the Groq LLM
for natural-language-to-SQL generation.
"""

from groq import Groq
from langsmith import traceable

from app.config import (
    GROQ_API_KEY,
    GROQ_MODEL,
)

from app.prompting.prompt_builder import (
    PromptBuilder,
)


class SQLGenerator:
    """
    Generates SQLite SQL queries from
    natural-language questions.
    """

    def __init__(
        self,
        schema: str,
    ) -> None:

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

        self.model = GROQ_MODEL

        self.prompt_builder = PromptBuilder(
            schema=schema
        )

    @traceable(
        name="SQL Generation",
        run_type="llm",
    )
    def generate(
        self,
        question: str,
    ) -> str:
        """
        Generate SQL for a natural-language question.
        """

        prompts = self.prompt_builder.build(
            question
        )

        response = self.client.chat.completions.create(
            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": prompts[
                        "system_prompt"
                    ],
                },
                {
                    "role": "user",
                    "content": prompts[
                        "user_prompt"
                    ],
                },
            ],

            temperature=0,
        )

        sql = response.choices[0].message.content

        if not sql:
            raise ValueError(
                "The LLM returned an empty response."
            )

        return self._clean_sql(
            sql
        )

    def _clean_sql(
        self,
        sql: str,
    ) -> str:
        """
        Remove Markdown code fences if the model
        returns them despite the instructions.
        """

        sql = sql.strip()

        if sql.startswith("```sql"):
            sql = sql[6:]

        elif sql.startswith("```"):
            sql = sql[3:]

        if sql.endswith("```"):
            sql = sql[:-3]

        return sql.strip()