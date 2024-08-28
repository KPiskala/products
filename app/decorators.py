"""
This module provides a decorator for retrying function calls
a specified number of times with a delay between retries.
"""

import time
from functools import wraps

from app.logger import get_logger

logger = get_logger(__name__)


def retry(retries: int, delay: float) -> callable:
    """
    A decorator that retries a function call a specified number of times with a delay.

    Args:
        retries (int): Number of times to retry the function.
        delay (float): Delay (in seconds) between retries.

    Returns:
        callable: The decorated function with retry logic.
    """

    def decorator(func: callable) -> callable:
        @wraps(func)
        def wrapper(*args: any, **kwargs: any) -> any:
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(
                        "Attempt %d/%d failed: %s. Retrying in %f seconds...",
                        i + 1,
                        retries,
                        e,
                        delay,
                    )
                    if i < retries - 1:
                        time.sleep(delay)
                    else:
                        logger.error("All %d attempts failed: %s", retries, e)
                        raise e

        return wrapper

    return decorator
