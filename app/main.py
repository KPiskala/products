"""
This module serves as the entry point for the application.
It loads environment variables, fetches product data from an API,
and answers a series of questions about the products.
"""

import os

from dotenv import load_dotenv

from app.calculations import (
    count_products,
    count_products_per_category,
    get_average_price_for_category,
    get_most_expensive_in_category,
)
from app.fetch_data import fetch_all_products
from app.models import Product
from app.utils import write_and_print


def answer_questions(products: list[Product], file_name: str) -> None:
    """
    Answer a series of questions about a list of products. Print them and save into file.

    Args:
        products (list[Product]): A list of Product objects to analyze.

    Prints:
        - Total number of products.
        - Number of products in each category.
        - Most expensive product in the 'Fashion' category.
        - Average price of products in the 'Toys & Games' category.
    """
    with open(file_name, "w", encoding="utf-8") as file:
        # 1. total number of products
        products_count = count_products(products)
        write_and_print(file, f"1. Number of products: {products_count}.")

        # 2. products in each category
        category_products_counts = count_products_per_category(products)
        counts_to_print = "\n\t".join(
            [
                f"In category '{category}' there are {number} products."
                for category, number in category_products_counts.items()
            ]
        )
        write_and_print(file, "2. " + counts_to_print)

        # 3. most expensive product in Fashion category
        most_expensive_in_fashion = get_most_expensive_in_category(products, "Fashion")
        if most_expensive_in_fashion:
            write_and_print(
                file,
                f"3. Most expensive fashion product is {most_expensive_in_fashion.product_name}"
                + f" (id: {most_expensive_in_fashion.product_id}).",
            )
        else:
            write_and_print(file, "3. There are no products in 'Fashion' category.")

        # 4. average price in Toys & Games category
        avg_price = get_average_price_for_category(products, "Toys & Games")
        if avg_price:
            write_and_print(
                file,
                f"4. The average price in 'Toys & Games' category is {round(avg_price, 2)} PLN.",
            )
        else:
            write_and_print(
                file, "4. There are no products of the 'Toys & Games' category."
            )


def main() -> None:
    """
    Main function to load environment variables, fetch products, and answer questions.
    """
    load_dotenv()
    api_url = os.getenv("API_URL")
    if api_url is None:
        raise ValueError("API_URL not found in environment variables")

    products = fetch_all_products(api_url)
    answer_questions(products, "answers.txt")


if __name__ == "__main__":
    main()
