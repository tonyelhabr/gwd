from sqlalchemy.orm import Session

from app.db import models, schemas


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
