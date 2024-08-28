"""
This module defines the Product model using Pydantic.
"""

from pydantic import BaseModel


class Product(BaseModel):
    """
    A model representing a product with various attributes.

    Attributes:
        product_id (int): The unique identifier for the product.
        product_name (str): The name of the product.
        category (str): The category to which the product belongs.
        price (float): The price of the product.
        currency (str): The currency of the price.
        next_product_token (str | None): A token for fetching the next product (if applicable).
    """

    product_id: int
    product_name: str
    category: str
    price: float
    currency: str
    next_product_token: str | None
