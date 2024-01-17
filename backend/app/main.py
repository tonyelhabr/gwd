from fastapi import FastAPI

from .api import venues, results

from .db import models
from .db.database import engine

import logging
from logging.config import dictConfig
from .extensions.logger import LogConfig, LOGGER_NAME

dictConfig(LogConfig().model_dump())

logger = logging.getLogger(LOGGER_NAME)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return "GeeksWhoDrink API"


app.include_router(venues.router)
app.include_router(results.router)
