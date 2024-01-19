from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import venues as v
from app.db import schemas
from app.db.database import get_db
from app.services.scraper import ScrapingService

import logging
from app.extensions.logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


router = APIRouter()


@router.post("/api/venues/", response_model=schemas.Venue)
def create_venue(venue: schemas.VenueCreate, db: Session = Depends(get_db)):
    # TODO: Just use get_venue here
    db_venue = v.get_venue_by_name(db, name=venue.name)
    if db_venue:
        raise HTTPException(status_code=400, detail="Venue name already used.")
    return v.create_venue(db=db, venue=venue)


@router.get("/api/venues/", response_model=list[schemas.Venue])
def read_venues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    venues = v.get_venues(db=db, skip=skip, limit=limit)
    return venues


@router.get("/api/venues/{source_id}", response_model=schemas.Venue)
def read_venue(source_id: int, db: Session = Depends(get_db)):
    db_venue = v.get_venue(db, source_id=source_id)
    if db_venue is None:
        raise HTTPException(status_code=404, detail="Venue name not found.")

    logger.info(f"Retrieved venue {db_venue.source_id}.")
    return db_venue


# TODO
# @router.get("/api/venues/lookup/{name}", response_model=schemas.Venue)
# def read_venue_by_name(venue_id: int, db: Session = Depends(get_db)):
#     db_venue = v.get_venue_by_name(db, venue_id=venue_id)
#     if db_venue is None:
#         raise HTTPException(status_code=404, detail="Venue name not found.")
#     logger.info(f"Retrieved venue {db_venue.name}.")
#     return db_venue


# TODO: Add authentication
@router.post("/api/scraping/test/venues")
def test_scraping_venues(db: Session = Depends(get_db)):
    ss = ScrapingService()
    logger.info("Starting to scrape venues.")
    scraped_venues = ss.scrape_venues()
    logger.info("Finished scraping venues.")
    for scraped_venue in scraped_venues:
        existing_venue = v.get_venue(db, source_id=scraped_venue.source_id)
        if not existing_venue:
            venue_data = schemas.VenueCreate(**scraped_venue)
            v.create_venue(db, venue_data)
        else:
            venue_data = schemas.VenueUpdate(**scraped_venue)
            v.update_venue(db, venue_data)
