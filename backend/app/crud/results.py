## Reference: https://github.com/tonyelhabr/jobcrawler/blob/master/backend/jobcrawler/crud/searches.py
from sqlalchemy.orm import Session
from typing import Optional
from app.db import models, schemas
from datetime import datetime

import logging
from app.extensions.logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def get_result(
    db: Session, source_id: str, limit: int = 100
) -> Optional[list[models.Result]]:
    return (
        db.query(models.Result)
        .filter(models.Result.source_id == source_id)
        .limit(limit)
        .all()
    )


def get_results(
    db: Session, skip: int = 0, limit: int = 100
) -> Optional[list[models.Result]]:
    return db.query(models.Result).offset(skip).limit(limit).all()


def create_result(db: Session, result: schemas.ResultCreate) -> Optional[models.Result]:
    logger.info(
        f"Creating a new result for source {result.source_id} and quiz_date {result.quiz_date}"
    )
    db_result = models.Result(
        quiz_date=result.quiz_date,
        team_name=result.team_name,
        ranking=result.ranking,
        score=result.score,
        source_id=result.source_id,
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


def update_result(
    db: Session, result: schemas.ResultUpdate
) -> Optional[list[models.Result]]:
    logger.info(f"Creating a new venue: {result.source_id}")
    db_result = (
        db.query(models.Result)
        .filter(models.Result.source_id == result.source_id)
        .first()
    )
    if not db_result:
        return None

    # Update existing venue
    for key, value in result.dict().items():
        setattr(db_result, key, value) if value else None

    # TODO: probably ok to remove this since we update it with `onupdate` in the model.
    db_result.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_result)
    return db_result
