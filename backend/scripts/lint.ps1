## Run with powershell ./scripts/lint.ps1
echo "Running Black ..."
poetry run black . 

echo "Running MyPy ..."
poetry run mypy .

echo "Running Ruff ..."
poetry run ruff check .
