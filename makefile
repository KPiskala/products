all: test black-check pylint-check mypy-check
	echo "All checks passed!"

style: isort black
	echo "Styles applied."

test:
	echo "Running tests..."
	python -m unittest discover tests/
	echo "Tests passed!"

black:
	echo "Running black..."
	black .
	echo "Black finished!"

isort:
	echo "Running isort..."
	isort .
	echo "Isort finished!"

black-check:
	echo "Checking black..."
	black --check .
	echo "Black passed!"

pylint-check:
	echo "Checking pylint..."
	find . -name '*.py' | xargs pylint
	echo "Pylint passed!"

mypy-check:
	echo "Checking mypy..."
	find . -name '*.py' | xargs mypy
	echo "Mypy passed!"

