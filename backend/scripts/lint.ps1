## Run with powershell ./scripts/lint.ps1
poetry run black . 
poetry run mypy .
poetry run ruff check .
