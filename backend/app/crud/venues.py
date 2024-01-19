from sqlalchemy.orm import Session
from typing import Optional
from app.db import models, schemas
from datetime import datetime

import logging
from app.extensions.logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def get_venue(db: Session, source_id: str) -> Optional[models.Venue]:
    return db.query(models.Venue).filter(models.Venue.source_id == source_id).first()


def get_venue_by_name(db: Session, name: str) -> Optional[models.Venue]:
    return db.query(models.Venue).filter(models.Venue.name == name).first()


def get_venues(db: Session, skip: int = 0, limit: int = 100) -> list[models.Venue]:
    return db.query(models.Venue).offset(skip).limit(limit).all()


def create_venue(db: Session, venue: schemas.VenueCreate) -> Optional[models.Venue]:
    db_venue = models.Venue(name=venue.name)
    db.add(db_venue)
    db.commit()
    db.refresh(db_venue)
    return db_venue


def update_venue(db: Session, venue: schemas.VenueUpdate) -> Optional[models.Venue]:
    db_venue = (
        db.query(models.Venue).filter(models.Venue.source_id == venue.source_id).first()
    )
    if not db_venue:
        return None

    # Update existing venue
    for key, value in venue.dict().items():
        setattr(db_venue, key, value) if value else None

    # TODO: probably ok to remove this since we update it with `onupdate` in the model.
    db_venue.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_venue)
    return db_venue
