"""
prompt_config.py

Configuration used by the NL-to-SQL prompt system.
"""

MAX_FEW_SHOT_EXAMPLES = 5

SQL_DIALECT = "SQLite"

ALLOWED_SQL_OPERATION = "SELECT"

MODEL_OUTPUT_FORMAT = "plain SQL only"