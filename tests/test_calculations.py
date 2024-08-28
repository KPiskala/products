"""
Unit tests for the calculations module. 

These tests cover functions for counting products, calculating average prices,
finding the most expensive products, and converting prices between currencies.
"""

import unittest
from unittest.mock import MagicMock, patch

from app.calculations import (
    count_products,
    count_products_per_category,
    get_average_price_for_category,
    get_most_expensive_in_category,
    get_price_in_currency,
)
from app.models import Product


class TestCalculations(unittest.TestCase):
    """
    Unit tests for functions in the app.calculations module.
    """

    def test_get_price_in_currency_same_currency(self) -> None:
        """
        Test the case when the original currency and the desired currency are the same.
        """
        price = 100.0
        currency = "USD"
        desired_currency = "USD"
        converted_price = get_price_in_currency(price, currency, desired_currency)
        self.assertEqual(price, converted_price)

    @patch("app.calculations.CurrencyConverter")
    def test_get_price_in_currency_different_currency(
        self, mock_currency_converter: MagicMock
    ) -> None:
        """
        Test conversion of price between different currencies using a mocked CurrencyConverter.
        """
        mock_converter = mock_currency_converter.return_value
        mock_converter.convert.return_value = 85.0

        price = 100.0
        currency = "USD"
        desired_currency = "EUR"

        converted_price = get_price_in_currency(
            price, currency, desired_currency, mock_converter
        )

        mock_converter.convert.assert_called_once_with(
            price, currency, desired_currency
        )
        self.assertEqual(converted_price, 85.0)

    def test_count_products(self) -> None:
        """
        Test counting the total number of products in a list.
        """
        products = [
            Product(
                product_id=1,
                product_name="Product 1",
                price=100.0,
                category="Category 1",
                currency="USD",
                next_product_token="dsdvsdfds",
            ),
            Product(
                product_id=2,
                product_name="Product 2",
                price=200.0,
                category="Category 2",
                currency="USD",
                next_product_token=None,
            ),
        ]
        self.assertEqual(count_products(products), 2)

    def test_count_products_per_category(self) -> None:
        """
        Test counting the number of products per category.
        """
        products = [
            Product(
                product_id=1,
                product_name="Product 1",
                price=100.0,
                category="Category 1",
                currency="USD",
                next_product_token="dsdvsdfds",
            ),
            Product(
                product_id=2,
                product_name="Product 2",
                price=200.0,
                category="Category 1",
                currency="USD",
                next_product_token="fsgfs",
            ),
            Product(
                product_id=3,
                product_name="Product 3",
                price=300.0,
                category="Category 2",
                currency="USD",
                next_product_token="gsrgsr",
            ),
        ]
        expected_counts = {"Category 1": 2, "Category 2": 1}
        self.assertEqual(count_products_per_category(products), expected_counts)

    @patch("app.calculations.get_price_in_currency")
    def test_get_most_expensive_in_category(
        self, mock_get_price_in_currency: MagicMock
    ) -> None:
        """
        Test finding the most expensive product in a given category
        using a mocked get_price_in_currency function.
        """
        mock_get_price_in_currency.side_effect = [400.0, 200.0]
        products = [
            Product(
                product_id=1,
                product_name="Product 1",
                price=100.0,
                category="Category 1",
                currency="USD",
                next_product_token="dsdvsdfds",
            ),
            Product(
                product_id=2,
                product_name="Product 2",
                price=200.0,
                category="Category 1",
                currency="USD",
                next_product_token="gdrgdfgd",
            ),
            Product(
                product_id=3,
                product_name="Product 3",
                price=300.0,
                category="Category 2",
                currency="USD",
                next_product_token="gsrgsr",
            ),
        ]
        most_expensive = get_most_expensive_in_category(products, "Category 1")
        self.assertEqual(most_expensive.product_id, 1)
        mock_get_price_in_currency.assert_any_call(100.0, "USD", "PLN")
        mock_get_price_in_currency.assert_any_call(200.0, "USD", "PLN")

    def test_get_most_expensive_in_category_no_products(self) -> None:
        """
        Test finding the most expensive product in a category when there are no products.
        """
        products = []
        most_expensive = get_most_expensive_in_category(products, "Category 1")
        self.assertIsNone(most_expensive)

    @patch("app.calculations.get_price_in_currency")
    def test_get_average_price_for_category(
        self, mock_get_price_in_currency: MagicMock
    ) -> None:
        """
        Test calculating the average price for products in a given category
        using a mocked get_price_in_currency function.
        """
        mock_get_price_in_currency.side_effect = [400.0, 600.0]
        products = [
            Product(
                product_id=1,
                product_name="Product 1",
                price=100.0,
                category="Category 1",
                currency="USD",
                next_product_token="dsdvsdfds",
            ),
            Product(
                product_id=2,
                product_name="Product 2",
                price=200.0,
                category="Category 1",
                currency="USD",
                next_product_token="gdrgdfgd",
            ),
            Product(
                product_id=3,
                product_name="Product 3",
                price=300.0,
                category="Category 2",
                currency="USD",
                next_product_token="gsrgsr",
            ),
        ]
        average_price = get_average_price_for_category(products, "Category 1")
        self.assertEqual(average_price, 500.0)
        mock_get_price_in_currency.assert_any_call(100.0, "USD", "PLN")
        mock_get_price_in_currency.assert_any_call(200.0, "USD", "PLN")

    def test_get_average_price_for_category_no_products(self) -> None:
        """
        Test calculating the average price for products in a category when there are no products.
        """
        products = []
        average_price = get_average_price_for_category(products, "Category 1")
        self.assertIsNone(average_price)


if __name__ == "__main__":
    unittest.main()
