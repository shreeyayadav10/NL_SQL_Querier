"""
logger.py

Creates a reusable logger for the project.
"""

import logging


def get_logger(logger_name: str):

    logger = logging.getLogger(logger_name)

    if not logger.handlers:

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger