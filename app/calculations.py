"""
This module contains functions for performing various calculations
related to products, such as counting products, finding the most expensive
product in a category, and calculating average prices. It also includes
a utility function for converting product prices between currencies.
"""

from currency_converter import CurrencyConverter

from app.models import Product

c = CurrencyConverter()


def get_price_in_currency(
    price: float, currency: str, desired_currency: str, converter: CurrencyConverter = c
) -> float:
    """
    Convert the price of a product from one currency to another using the provided converter.

    Args:
        price (float): The price of the product in the original currency.
        currency (str): The original currency code (e.g., "USD").
        desired_currency (str): The desired currency code (e.g., "EUR").
        converter (CurrencyConverter): The currency converter instance to use for conversion.

    Returns:
        float: The price of the product in the desired currency.
    """
    if currency == desired_currency:
        return price
    return converter.convert(price, currency, desired_currency)


def count_products(products: list[Product]) -> int:
    """
    Count the total number of products.

    Args:
        products (list[Product]): A list of Product objects.

    Returns:
        int: The total number of products in the list.
    """
    return len(products)


def count_products_per_category(products: list[Product]) -> dict[str, int]:
    """
    Count the number of products in each category.

    Args:
        products (list[Product]): A list of Product objects.

    Returns:
        dict[str, int]: A dictionary where keys are category names and values
        are the count of products in each category.
    """
    category_products_counts = {}
    for product in products:
        category_products_counts[product.category] = (
            category_products_counts.get(product.category, 0) + 1
        )
    return category_products_counts


def get_most_expensive_in_category(
    products: list[Product], category: str
) -> Product | None:
    """
    Find the most expensive product in a specific category.

    Args:
        products (list[Product]): A list of Product objects.
        category (str): The category for which maximum price should be found.

    Returns:
        Product | None: The most expensive Product object in the specified category,
        or None if no products are found.
    """
    category_products = [p for p in products if p.category == category]
    if not category_products:
        return None
    return max(
        category_products,
        key=lambda x: get_price_in_currency(x.price, x.currency, "PLN"),
    )


def get_average_price_for_category(
    products: list[Product], category: str
) -> float | None:
    """
    Calculate the average price of products in a specific category.

    Args:
        products (list[Product]): A list of Product objects.
        category (str): The category to calculate the average price for.

    Returns:
        float | None: The average price of products in the specified category,
        or None if no products are found.
    """
    category_products = [p for p in products if p.category == category]
    if not category_products:
        return None
    return sum(
        get_price_in_currency(product.price, product.currency, "PLN")
        for product in category_products
    ) / len(category_products)
