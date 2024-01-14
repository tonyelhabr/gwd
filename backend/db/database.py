## https://fastapi.tiangolo.com/tutorial/sql-databases/
from config import Settings

from contextlib import contextmanager
from warnings import warn

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


settings = Settings()

SQLALCHEMY_DATABASE_URL = settings.database_url

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def SessionManager():
    db = SessionLocal()
    try:
        yield db
    except:
        # if we fail somehow rollback the connection
        warn("We somehow failed in a DB operation and auto-rollbacking...")
        db.rollback()
        raise
    finally:
        db.close()
