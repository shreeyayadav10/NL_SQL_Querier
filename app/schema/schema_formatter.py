"""
schema_formatter.py

Converts the structured database metadata into a readable
text representation suitable for an LLM prompt.
"""

from app.schema.schema_inspector import SchemaInspector


class SchemaFormatter:

    def __init__(self):

        self.inspector = SchemaInspector()

    def format_schema(self) -> str:
        """
        Convert database metadata into LLM-friendly text.
        """

        schema = self.inspector.inspect_database()

        sections = []

        sections.append(
            "DATABASE SCHEMA\n"
            "===============\n"
        )

        for table_name, table_info in schema.items():

            table_section = []

            table_section.append(
                f"TABLE: {table_name}"
            )

            table_section.append(
                "COLUMNS:"
            )

            for column in table_info["columns"]:

                column_name = column["name"]

                data_type = column["type"]

                nullable = column["nullable"]

                column_description = (
                    f"  - {column_name}: "
                    f"{data_type}"
                )

                if column_name in table_info[
                    "primary_keys"
                ]:

                    column_description += (
                        " [PRIMARY KEY]"
                    )

                if nullable:

                    column_description += (
                        " [NULLABLE]"
                    )

                samples = column[
                    "sample_values"
                ]

                if samples:

                    formatted_samples = ", ".join(
                        str(value)
                        for value in samples
                    )

                    column_description += (
                        f" | Examples: "
                        f"{formatted_samples}"
                    )

                table_section.append(
                    column_description
                )

            foreign_keys = table_info[
                "foreign_keys"
            ]

            if foreign_keys:

                table_section.append(
                    "RELATIONSHIPS:"
                )

                for foreign_key in foreign_keys:

                    source_columns = ", ".join(
                        foreign_key["columns"]
                    )

                    target_columns = ", ".join(
                        foreign_key["referred_columns"]
                    )

                    relationship = (
                        f"  - {source_columns} "
                        f"→ "
                        f"{foreign_key['referred_table']}"
                        f".{target_columns}"
                    )

                    table_section.append(
                        relationship
                    )

            sections.append(
                "\n".join(table_section)
            )

        return "\n\n".join(sections)


if __name__ == "__main__":

    formatter = SchemaFormatter()

    schema_context = formatter.format_schema()

    print(schema_context)