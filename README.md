![Lifecycle: work in progress](https://img.shields.io/badge/lifecycle-work%20in%20progress-blue.svg)

# GeeksWhoDrink API

[GeeksWhoDrink API]() is a FastAPI for serving [GeeksWhoDrink](https://www.geekswhodrink.com/) pub trivia quiz results.

## Getting Started

```bash
poetry install
```

```bash
cd backend && poetry run uvicorn gwd.main:app
```

Then navigate to `http://127.0.0.1:8000/docs#/operation` in your browser.
