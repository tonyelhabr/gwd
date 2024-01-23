#! /bin/bash

eval $(./node_modules/.bin/dotenvenc -x -i config/.env.enc.dev)

python -m pytest tests/
