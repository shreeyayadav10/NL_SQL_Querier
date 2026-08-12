"""
schema_cache.py

Creates and loads a cached copy of the database schema.
"""

import json
from pathlib import Path

from app.schema.schema_inspector import SchemaInspector


CACHE_DIR = Path("cache")
CACHE_FILE = CACHE_DIR / "schema_cache.json"


class SchemaCache:

    def __init__(self):

        CACHE_DIR.mkdir(exist_ok=True)

        self.inspector = SchemaInspector()

    def create_cache(self):

        schema = self.inspector.inspect_database()

        with open(
            CACHE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                schema,
                file,
                indent=4,
                ensure_ascii=False
            )

        print("Schema cache created.")

    def load_cache(self):

        if not CACHE_FILE.exists():

            self.create_cache()

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


if __name__ == "__main__":

    cache = SchemaCache()

    cache.create_cache()