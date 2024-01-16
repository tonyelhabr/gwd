FROM python:3.11-slim-bullseye

COPY . .

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1 
ENV POETRY_VERSION=1.5.0

RUN apt-get update \
    && apt-get install -y wget gnupg2 curl \
    && rm -rf /var/lib/apt/lists/*
    
RUN apt-get install -y gcc

RUN pip install poetry==${POETRY_VERSION} && \
    poetry config virtualenvs.path --unset && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-root --no-dev

EXPOSE 8000

CMD ["./scripts/start.sh"]
