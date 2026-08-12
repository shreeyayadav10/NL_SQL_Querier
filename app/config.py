"""
Application configuration.

Loads configuration values from environment variables.
"""

import os

from dotenv import load_dotenv


# ==========================================================
# Load environment variables
# ==========================================================

load_dotenv()


# ==========================================================
# Groq configuration
# ==========================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)


# ==========================================================
# LangSmith configuration
# ==========================================================

LANGCHAIN_API_KEY = os.getenv(
    "LANGCHAIN_API_KEY"
)

LANGCHAIN_PROJECT = os.getenv(
    "LANGCHAIN_PROJECT",
    "NL_SQL_QUERIER",
)

LANGCHAIN_TRACING_V2 = os.getenv(
    "LANGCHAIN_TRACING_V2",
    "true",
).lower() == "true"


# ==========================================================
# Configuration validation
# ==========================================================

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not configured. "
        "Add it to the .env file."
    )