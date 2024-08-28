# Products

## Description

The Products project is designed to fetch, analyze, and report on product data retrieved from an external API. The main functionalities include:

- **Data Retrieval**: Fetches product data from a specified API.
- **Data Analysis**: Processes the product data to answer specific questions:
  - Total number of products.
  - Number of products per category.
  - Most expensive product in the "Fashion" category.
  - Average price of products in the "Toys & Games" category (rounded; approximate if any price is in a currency different than PLN).
- **Output**: Saves the analysis results to a file and prints them to the console.

### Features

- Count and categorize products.
- Identify the most expensive product in a specific category.
- Compute the average price for a category.
- Save results to `answers.txt` and print them.

## Prerequisites

- Docker
- Docker Compose

## Clone the Repository

To get started, clone the repository using the following command:

```bash
git clone https://github.com/KPiskala/products.git
cd products
```

## Running the Application

1. **Build and run the application**:

   Use Docker Compose to build and start the application service. This will also run the `main.py` script:

   ```bash
   docker compose up
   ```

   This command will:
   - Build the Docker image defined in `Dockerfile`.
   - Start the `app` service and run the `main.py` script.
   - Create or update an `answers.txt` file with the results of the analysis.
   - Print the results to the console.

2. **Accessing the results**:

   After running the application, check the `answers.txt` file for the analysis results. It will contain:
   - The total number of products.
   - The number of products in each category.
   - The most expensive product in the "Fashion" category.
   - The average price of products in the "Toys & Games" category.

    P.S. You can also check the `answers.txt` file now to check the results if you don't feel like running the application.

## Running Tests

**Build and run the checks**:

   To run tests and checks, use the following command:

   ```bash
   docker compose run --rm checks make all
   ```

## Viewing Logs

To view logs for the running application, use:

   ```bash
   docker compose logs
   ```

To view logs specifically for the `app` service, use:

   ```bash
   docker compose logs app
   ```

## Project Structure

- `app/`
  - `calculations.py`: Contains functions for product data analysis - finding the mean, maximum, converting the prices to other currency, etc.
  - `decorators.py`: Contains a decorator for retrying the function call.
  - `fetch_data.py`: Contains functions to fetch product(s) data from the API.
  - `logger.py`: Handles logging.
  - `main.py`: Entry point of the application, loads environment variables, fetches data, and answers the questions.
  - `models.py`: Contains the `Product` class definition.
  - `utils.py`: Utility functions, including `write_and_print` which allows to print results and save them into file at the same time.

- `config/`
  - `config.yml`: Configuration file.

- `tests/`
  - `test_calculations.py`: Tests for `calculations.py`.
  - `test_decorators.py`: Tests for `decorators.py`.
  - `test_fetch_data.py`: Tests for `fetch_data.py`.

- `.env`: Environment variables file, including `API_URL` - hidden.
- `.gitignore`: Specifies files and directories to be ignored by Git.
- `.requirements_dev.txt`: Development dependencies.
- `answers.txt`: File where the analysis results are saved. It contains ready answers if you want to just see them but you can also create a fresh content by runing the app.
- `docker-compose.yml`: Docker Compose configuration.
- `Dockerfile`: Defines the Docker image for the application.
- `makefile`: Commands for running tests and other checks.
- `requirements.txt`: Production dependencies.

## Project Assumptions

To provide a robust solution for the task, the following assumptions were made:

1. **No Database Storage**:
   - For this task, products are processed in-memory rather than being saved to a database. This approach simplifies the solution and fits the task requirements, which focus on data retrieval and processing rather than persistent storage.

2. **Handling API Failures**:
   - The script includes basic error handling for API failures, such as retrying requests in case of temporary issues or handling `503 Service Unavailable` responses. This ensures that the script can handle intermittent problems with the API service.

3. **Data Retrieval**:
   - The script retrieves products sequentially until no more products are available (indicated by an empty `next_product_token`). It uses the token provided by the API to fetch the next product, ensuring all products are collected.

4. **Data Analysis**:
   - The analysis of products is performed in-memory once all data is fetched. This approach is feasible given the nature of the task and avoids the complexity of managing a database.

5. **Environment Configuration**:
   - The API URL is provided through environment variables, which is a common practice for managing configuration. This allows the script to be easily adapted to different environments or API endpoints.

6. **Code Quality**:
   - The code adheres to Python best practices, including proper error handling, clear and maintainable code structure, and the use of functions and modules to organize the script effectively.

7. **Testing**:
   - Tests are written to ensure the correctness of the data processing and analysis functions. This helps in verifying that the script performs as expected and handles edge cases appropriately.

These assumptions guide the implementation and ensure that the solution meets the task requirements while adhering to best practices for coding and data processing.
