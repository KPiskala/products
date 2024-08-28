"""
This module provides functions to fetch products from an API.
It includes functionality to fetch a single product as well as all products.
"""

import requests

from app.decorators import retry
from app.logger import get_logger
from app.models import Product
from app.utils import load_config

logger = get_logger(__name__)

config = load_config("config/config.yml")


@retry(retries=config["api"]["retries"], delay=config["api"]["delay"])
def fetch_product(api_url: str, token: str | None = None) -> Product:
    """
    Fetch a single product from the API.

    Args:
        api_url (str): The URL of the API endpoint.
        token (str | None): The token for the next product (for pagination), if any.

    Returns:
        Product: The product data converted to a Product model.
    """
    logger.info("Fetching data for token %s.", token)
    params = {"next_product_token": token} if token else {}
    response = requests.get(api_url, params=params, timeout=config["api"]["timeout"])
    if response.status_code == 503:
        logger.warning("Service unavailable (503). Retrying...")
        response.raise_for_status()
    response.raise_for_status()
    product_data = response.json()
    logger.info("Data accessed.")
    return Product(**product_data)


def fetch_all_products(api_url: str, token: str = None) -> list[Product]:
    """
    Fetch all products from the API.

    Args:
        api_url (str): The URL of the API endpoint.
        token (str): The product token.

    Returns:
        list[Product]: A list of all products fetched from the API.
    """
    products = []
    logger.info("Fetching products.")

    while True:
        product = fetch_product(api_url, token)
        products.append(product)
        token = product.next_product_token
        if not token:
            break

    logger.info("All products have been fetched.")

    return products
