"""
This module provides a function to get a configured logger instance.
It sets up logging with a specific format and logging level.
"""

import logging
from logging import Logger


def get_logger(name: str) -> Logger:
    """
    Get a configured logger.

    Args:
        name (str): The name of the logger.

    Returns:
        Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
