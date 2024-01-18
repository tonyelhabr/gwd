#! /bin/bash

echo "Running Black ..."
poetry run black . 

echo "Running MyPy ..."
poetry run mypy .

echo "Running Ruff ..."
poetry run ruff check .
