#! /bin/bash

python -m app.backend_pre_start
alembic upgrade head
python -m app.initial_data
uvicorn app.main:app --host "0.0.0.0"
