import logging
from sqlalchemy import text
from app.extensions.logger import LOGGER_NAME

from app.db.database import SessionLocal

logger = logging.getLogger(LOGGER_NAME)


def init() -> None:
    try:
        db = SessionLocal()
        logger.info("Trying to create a session to check if DB is awake")
        db.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
