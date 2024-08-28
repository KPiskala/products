"""
This module provides utility functions for loading YAML configuration 
and writing messages to a file.
"""

from typing import Any, TextIO

import yaml


def load_config(file_path: str) -> dict[str, Any]:
    """
    Load and parse a YAML configuration file.

    Args:
        file_path (str): The path to the YAML configuration file.

    Returns:
        dict[str, Any]: A dictionary containing the configuration data loaded from the YAML file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def write_and_print(file: TextIO, message: str) -> None:
    """
    Write a message to a file and print it to the console.

    Args:
        file (TextIO): The file object to write to.
        message (str): The message to write and print.
    """
    print(message)
    file.write(message + "\n")
