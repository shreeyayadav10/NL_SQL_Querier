"""
sql_corrector.py

Attempts to correct SQL queries that fail during execution.
"""

from groq import Groq

from app.config import GROQ_API_KEY, GROQ_MODEL


class SQLCorrector:
    """
    Uses the LLM to correct an SQL query after execution failure.
    """

    def __init__(self, schema: str) -> None:

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

        self.model = GROQ_MODEL
        self.schema = schema

    def correct(
        self,
        question: str,
        failed_sql: str,
        error_message: str,
    ) -> str:
        """
        Generate a corrected SQL query.
        """

        system_prompt = """
You are an expert SQLite SQL analyst.

Your task is to correct a SQL query that failed during execution.

Rules:

1. Return SQLite-compatible SQL only.
2. Return exactly ONE SELECT statement.
3. Never use INSERT, UPDATE, DELETE, DROP,
   ALTER, CREATE, TRUNCATE, ATTACH, or PRAGMA.
4. Use only tables and columns from the provided schema.
5. Preserve the original user's intent.
6. Use the execution error to identify and fix the problem.
7. Do not invent tables or columns.
8. Return ONLY the corrected SQL query.
9. Do not use Markdown code fences.
10. Do not provide explanations.
"""

        user_prompt = f"""
DATABASE SCHEMA
===============

{self.schema}

USER QUESTION
=============

{question}

FAILED SQL
==========

{failed_sql}

EXECUTION ERROR
===============

{error_message}

TASK
====

Correct the SQL query so that it answers the user's
question and can execute successfully against the
provided SQLite database.

Return ONLY the corrected SQL query.
"""

        response = self.client.chat.completions.create(
            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],

            temperature=0,
        )

        sql = response.choices[0].message.content

        if not sql:
            raise ValueError(
                "The LLM returned an empty correction."
            )

        return self._clean_sql(sql)

    def _clean_sql(self, sql: str) -> str:
        """
        Remove Markdown code fences if returned by the model.
        """

        sql = sql.strip()

        if sql.startswith("```sql"):
            sql = sql[6:]

        elif sql.startswith("```"):
            sql = sql[3:]

        if sql.endswith("```"):
            sql = sql[:-3]

        return sql.strip()