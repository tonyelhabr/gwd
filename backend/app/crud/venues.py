from sqlalchemy.orm import Session

from app.db import models, schemas
from datetime import datetime


def get_venue(db: Session, venue_id: int):
    return db.query(models.Venue).filter(models.Venue.id == venue_id).first()


def get_venue_by_name(db: Session, name: str):
    return db.query(models.Venue).filter(models.Venue.name == name).first()


def get_venues(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Venue).offset(skip).limit(limit).all()


def create_venue(db: Session, venue: schemas.VenueCreate):
    db_venue = models.Venue(name=venue.name)
    db.add(db_venue)
    db.commit()
    db.refresh(db_venue)
    return db_venue


def upsert_venue(db: Session, venue: schemas.VenueCreate):
    db_venue = (
        db.query(models.Venue).filter(models.Venue.source_id == venue.source_id).first()
    )
    if db_venue:
        # Update existing venue
        for key, value in venue.dict().items():
            setattr(db_venue, key, value)
        # TODO: probably ok to remove this since we update it with `onupdate` in the model.
        db_venue.updated_at = (
            datetime.utcnow()
        )  # explicitly update the 'updated_at' field
    else:
        # Create new venue
        db_venue = models.Venue(**venue.dict())
        db.add(db_venue)

    db.commit()
    db.refresh(db_venue)
    return db_venue
