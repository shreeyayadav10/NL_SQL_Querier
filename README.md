# NL SQL Querier

An AI-powered Natural Language to SQL analytics application that allows users to query e-commerce data using plain English instead of writing SQL manually.

The application uses the Olist Brazilian E-Commerce dataset and combines Large Language Models, LangChain, Groq, SQL validation, SQL correction, SQLite, and Streamlit to provide an end-to-end natural-language analytics workflow.

## Live Demo

[https://nlsqlquerier.streamlit.app/](https://nlsqlquerier.streamlit.app/)

## GitHub Repository

[https://github.com/shreeyayadav10/NL_SQL_Querier](https://github.com/shreeyayadav10/NL_SQL_Querier)

---

## Overview

NL SQL Querier is designed to make database analytics more accessible to users who may not have advanced SQL knowledge.

A user can enter a question such as:

> What are the top 10 product categories by number of products?

The application understands the question, generates the corresponding SQL query, validates it, executes it against the Olist SQLite database, and presents the results in a readable format with visualizations and analytical insights.

### Workflow

```text
Natural Language Question
            ↓
      Schema Inspection
            ↓
       SQL Generation
            ↓
       SQL Validation
            ↓
       SQL Correction
            ↓
       SQL Execution
            ↓
      Result Formatting
            ↓
        Visualization
            ↓
      Business Insights