#! /bin/bash

python /app/backend_pre_start.py
echo 'before alembic'
alembic upgrade head
# uvicorn app.main:app --host "0.0.0.0"
echo 'after alembic'
python /app/initial_data.py
