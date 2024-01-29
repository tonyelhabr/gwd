from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import List
from app.crud import results as r
from app.db import schemas
from app.db.database import get_db
from app.services.scraper import ResultsScrapingService

import logging
from app.extensions.logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

router = APIRouter()


# TODO: Add authentication
@router.post("/api/result/", response_model=schemas.Result)
def create_results_for_venue_quiz_date(
    result: schemas.ResultCreate, db: Session = Depends(get_db)
):
    return r.create_result(db=db, result=result)


@router.get("/api/result/", response_model=List[schemas.Result])
def read_results(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_results = r.get_all_results(db=db, skip=skip, limit=limit)
    return db_results


@router.get("/api/result/{source_id}", response_model=List[schemas.Result])
def read_results_for_venue(source_id: str, db: Session = Depends(get_db)):
    db_results = r.get_results_for_venue(db, source_id=source_id)
    if db_results is None:
        raise HTTPException(
            status_code=404, detail=f"Venue source ID '{source_id}' not found."
        )

    logger.info(f"Retrieved venue ID {source_id}.")
    return db_results


# TODO: Add authentication
@router.post("/api/scraping/test/result/{source_id}")
def test_scraping_results(source_id: str, db: Session = Depends(get_db)):
    rss = ResultsScrapingService(source_id=source_id)
    logger.info("Starting to scrape results.")
    scraped_results = rss.scrape_results(source_id=source_id)
    logger.info("Finished scraping results.")
    logger.info(f"Found {len(scraped_results)} results.")
    for scraped_result in scraped_results:
        existing_result = r.get_atomic_result(
            db,
            source_id=scraped_result["source_id"],
            quiz_week=scraped_result["quiz_week"],
            team_name=scraped_result["team"],
        )
        if not existing_result:
            logger.info(
                f"Result for venue ID {scraped_result['source_id']}, quiz date {scraped_result['quiz_date']}, team {scraped_result['team_name']} does not exist in the DB, so creating it."
            )
            result_to_create = schemas.ResultCreate(**scraped_result)
            r.create_result(db, result_to_create)
        else:
            logger.info(
                f"Result for venue ID {scraped_result['source_id']}, quiz date {scraped_result['quiz_date']}, team {scraped_result['team_name']} exists in the DB, so updating it."
            )
            result_to_update = schemas.ResultUpdate(**scraped_result)
            r.update_result(db, result_to_update)
