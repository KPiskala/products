"""
Unit tests for the retry decorator.

These tests cover the functionality of the retry decorator, including
success cases, failure cases, and varying retry delays.
"""

import unittest
from unittest.mock import MagicMock

from app.decorators import retry


class TestRetryDecorator(unittest.TestCase):
    """
    Unit tests for the retry decorator.
    """

    def test_retry_success(self) -> None:
        """
        Test that the decorated function is retried the correct number of times if it succeeds.
        """
        mock_func = MagicMock(return_value="success")
        decorated_func = retry(retries=3, delay=1)(mock_func)

        result = decorated_func()

        self.assertEqual(result, "success")
        self.assertEqual(mock_func.call_count, 1)  # Should only be called once

    def test_retry_failure(self) -> None:
        """
        Test that the decorated function retries the correct number of times
        and eventually raises an exception.
        """
        mock_func = MagicMock(side_effect=Exception("Test exception"))
        decorated_func = retry(retries=3, delay=1)(mock_func)

        with self.assertRaises(Exception) as context:
            decorated_func()

        self.assertEqual(str(context.exception), "Test exception")
        self.assertEqual(mock_func.call_count, 3)  # Should be called 3 times

    def test_retry_with_different_delays(self) -> None:
        """
        Test that the decorated function retries the correct number of times with different delays.
        """
        mock_func = MagicMock(side_effect=Exception("Test exception"))
        decorated_func = retry(retries=2, delay=0.1)(mock_func)

        with self.assertRaises(Exception) as context:
            decorated_func()

        self.assertEqual(str(context.exception), "Test exception")
        self.assertEqual(mock_func.call_count, 2)  # Should be called 2 times


if __name__ == "__main__":
    unittest.main()
