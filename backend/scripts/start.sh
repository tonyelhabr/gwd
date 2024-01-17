#! /bin/bash

# Let the DB start
python /app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python /app/initial_data.py

uvicorn app.main:app --host "0.0.0.0"
