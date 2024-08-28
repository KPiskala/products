"""
Unit tests for the fetch_data module.

These tests cover functionality for fetching products from the API, including
fetching a single product and fetching all products.
"""

import unittest
from unittest.mock import MagicMock, patch

from app.fetch_data import fetch_all_products, fetch_product
from app.models import Product


class TestFetchFunctions(unittest.TestCase):
    """
    Unit tests for the fetch_product and fetch_all_products functions.
    """

    # Class-level attributes for common test data
    product1 = Product(
        product_id=1,
        product_name="Test Product",
        category="Test Category",
        price=99.99,
        currency="USD",
        next_product_token="blablablab",
    )
    product2 = Product(
        product_id=2,
        product_name="Product 2",
        price=200.0,
        category="Category 2",
        currency="USD",
        next_product_token=None,
    )

    @patch("app.fetch_data.load_config")
    @patch("app.fetch_data.requests.get")
    def test_fetch_product_success(
        self, mock_requests_get: MagicMock, mock_load_config: MagicMock
    ) -> None:
        """
        Test that fetch_product correctly processes a successful API response.
        """
        # Mock configuration
        mock_load_config.return_value = {
            "api": {"timeout": 5, "retries": 3, "delay": 1}
        }

        # Setup mock for a successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "product_id": 2,
            "product_name": "Product 2",
            "category": "Category 2",
            "price": 200.0,
            "currency": "USD",
            "next_product_token": None,
        }
        mock_requests_get.return_value = mock_response

        api_url = "http://testapi.com/product"
        product = fetch_product(api_url)

        expected_product = self.product2

        self.assertEqual(product, expected_product)
        # Assert that requests.get was called with the expected URL and params
        args, kwargs = mock_requests_get.call_args
        self.assertEqual(args[0], api_url)
        self.assertEqual(kwargs.get("params"), {})

    @patch("app.fetch_data.fetch_product")
    def test_fetch_all_products(self, mock_fetch_product: MagicMock) -> None:
        """
        Test that fetch_all_products correctly processes multiple products.
        """
        # Setup mock fetch_product to return multiple products
        mock_fetch_product.side_effect = [
            self.product1,  # First call returns product1 with next_token
            self.product2,  # Second call returns product2 with no next_token
        ]

        api_url = "http://testapi.com/products"
        products = fetch_all_products(api_url)

        print("products", products)

        self.assertEqual(len(products), 2)
        self.assertEqual(products[0].product_id, 1)
        self.assertEqual(products[1].product_id, 2)
        mock_fetch_product.assert_called()

    @patch("app.fetch_data.fetch_product")
    def test_fetch_all_products_empty(self, mock_fetch_product: MagicMock) -> None:
        """
        Test that fetch_all_products handles the case where only one product is returned
        and no further products need to be retrieved.
        """
        # Setup mock to return no further products
        mock_fetch_product.return_value = Product(
            product_id=1,
            product_name="Product 1",
            price=100.0,
            category="Category 1",
            currency="USD",
            next_product_token=None,
        )

        api_url = "http://testapi.com/products"
        products = fetch_all_products(api_url)

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].product_id, 1)
        mock_fetch_product.assert_called_once()


if __name__ == "__main__":
    unittest.main()
