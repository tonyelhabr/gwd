from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import venues as v
from app.db import schemas
from app.db.database import get_db


import logging
from app.extensions.logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


router = APIRouter()


@router.post("/venues/", response_model=schemas.Venue)
def create_venue(venue: schemas.VenueCreate, db: Session = Depends(get_db)):
    db_venue = v.get_venue_by_name(db, name=venue.name)
    if db_venue:
        raise HTTPException(status_code=400, detail="Venue name already used.")
    return v.create_venue(db=db, venue=venue)


@router.get("/venues/", response_model=list[schemas.Venue])
def read_venues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    venues = v.get_venues(db=db, skip=skip, limit=limit)
    return venues


@router.get("/venues/{venue_id}", response_model=schemas.Venue)
def read_venue(venue_id: int, db: Session = Depends(get_db)):
    db_venue = v.get_venue(db, venue_id=venue_id)
    if db_venue is None:
        raise HTTPException(status_code=404, detail="Venue name not found.")

    logger.info(f"Retrieved venue {db_venue.venue_id}.")
    return db_venue
