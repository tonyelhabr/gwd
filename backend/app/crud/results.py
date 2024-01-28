## Reference: https://github.com/tonyelhabr/jobcrawler/blob/master/backend/jobcrawler/crud/searches.py
from sqlalchemy.orm import Session

from app.db import models, schemas


def get_results(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Result).offset(skip).limit(limit).all()


def create_result(db: Session, result: schemas.ResultCreate, source_id: str):
    db_result = models.Result(
        quiz_date=result.quiz_date,
        team_name=result.team_name,
        ranking=result.ranking,
        score=result.score,
        source_id=source_id,
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result
