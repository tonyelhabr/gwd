import logging
from app.extensions.logger import LOGGER_NAME

from app.db.database import SessionLocal, engine
from sqlalchemy.orm import Session

from app.crud import venues as v
from app.db import schemas

from app.db.database import Base  # noqa: F401

logger = logging.getLogger(LOGGER_NAME)


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)
    logger.info("Creating initial data")
    init_source_id = "x123"
    existing_venue = v.get_venue(db, source_id=init_source_id)
    if not existing_venue:
        logger.info(f"Venue {existing_venue} does not exist in the DB, so creating it.")
        venue_to_create = schemas.VenueCreate(
            source_id=init_source_id,
            name="foo",
            url="https://foo.com",
            lat=30.266666,
            lon=-97.733330,
            address="123 Main St. Austin TX",
        )
        v.create_venue(db, venue=venue_to_create)


def init() -> None:
    db = SessionLocal()
    init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
