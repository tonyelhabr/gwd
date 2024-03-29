from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import results as r
from app.db import schemas
from app.db.database import get_db

router = APIRouter()


# TODO: Add authentication
@router.post("/api/venues/{venue_id}/results/", response_model=schemas.Result)
def create_results_for_venue(
    venue_id: int, result: schemas.ResultCreate, db: Session = Depends(get_db)
):
    return r.create_result(db=db, result=result, venue_id=venue_id)


@router.get("/api/results/", response_model=list[schemas.Result])
def read_results(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_results = r.get_results(db=db, skip=skip, limit=limit)
    return db_results
