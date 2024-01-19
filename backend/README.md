# Backend

## Getting Started

### Quick start

From the `/backend/` folder, run

```bash
poetry run alembic upgrade head && poetry run uvicorn app.main:app
```

Then navigate to `http://127.0.0.1:8000/docs#/operation` in your browser.

### Docker approach

A more full-proof approach would be to use the docker-compose file.

```bash
docker-compose up --build
```

As before, navigate to `http://127.0.0.1:8000/docs#/operation` in your browser.

Note that, in the `Dockerfile` for the backend, we end up converting the poetry lock file to a more traditional pip requirements file. This has speed benefits, but means that we can't assume a poetry shell for Bash scripts.

Don't forget to terminate the Docker services!

```bash
docker-compose down
```

And if you want to remove the postgres volume (to prevent data from persisteng across lifecycles of a container), you can run

```bash
docker-compose down -v
```

If you were using sqlite or just wanted to debug something, you could also build the Dockerfile with just

```
docker build -t backend .
```

and run it with

```
docker run -p 8000:8000
```

or interactively with

```
docker run -it --entrypoint bash backend
```

## Gotchas

When editing Bash scripts, make sure the line endings are Linux-compatible. (Use Notepad++ if you're on Windows!)
