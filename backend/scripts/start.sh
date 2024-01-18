#! /bin/bash

eval $(./node_modules/.bin/dotenvenc -x -i config/.env.enc.dev)

python -m app.backend_pre_start && \
  alembic upgrade head && \
  python -m app.initial_data && \
  uvicorn app.main:app --host "0.0.0.0"
