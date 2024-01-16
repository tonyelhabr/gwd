#! /bin/bash

poetry run alembic upgrade head && \
poetry run uvicorn jobcrawler.main:app --host "0.0.0.0"
