import logging
from .extensions.logger import LOGGER_NAME

from .db.database import SessionLocal

from sqlalchemy.orm import Session

from .crud import venues as v
from .db import schemas

# from .db.database import Base  # noqa: F401


logger = logging.getLogger(LOGGER_NAME)


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    venue = v.get_venue_by_name(db, name="foo")
    if not venue:
        venue_to_create = schemas.VenueCreate(name="foo")
        venue = v.create_venue(db, venue=venue_to_create)


def init() -> None:
    db = SessionLocal()
    init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
