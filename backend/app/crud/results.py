from sqlalchemy.orm import Session

from app.db import models, schemas


def get_results(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Result).offset(skip).limit(limit).all()


def create_result(db: Session, result: schemas.ResultCreate, venue_id: int):
    db_result = models.Result(**result.dict(), venue_id=venue_id)
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result
