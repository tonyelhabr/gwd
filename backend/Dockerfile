FROM python:3.11-slim as requirements-stage

WORKDIR /tmp

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1 
ENV POETRY_VERSION=1.5.0

RUN pip install poetry==${POETRY_VERSION}

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-slim

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

EXPOSE 8000

CMD ["./scripts/start.sh"]
