from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .crud import venues as v
from .crud import results as r
from .db import models, schemas
from .db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return "GeeksWhoDrink API"


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/venues/", response_model=schemas.Venue)
def create_venue(venue: schemas.VenueCreate, db: Session = Depends(get_db)):
    db_venue = v.get_venue_by_name(db, name=venue.name)
    if db_venue:
        raise HTTPException(status_code=400, detail="Venue name already used.")
    return v.create_venue(db=db, venue=venue)


@app.get("/venues/", response_model=list[schemas.Venue])
def read_venues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    venues = v.get_venues(db=db, skip=skip, limit=limit)
    return venues


@app.get("/venues/{venue_id}", response_model=schemas.Venue)
def read_venue(venue_id: int, db: Session = Depends(get_db)):
    db_venue = v.get_venue(db, venue_id=venue_id)
    if db_venue is None:
        raise HTTPException(status_code=404, detail="Venue name not found.")
    return db_venue


@app.post("/venues/{venue_id}/results/", response_model=schemas.Result)
def create_results_for_venue(
    venue_id: int, result: schemas.ResultCreate, db: Session = Depends(get_db)
):
    return r.create_venue_result(db=db, result=result, venue_id=venue_id)


@app.get("/results/", response_model=list[schemas.Result])
def read_results(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    results = r.get_results(db=db, skip=skip, limit=limit)
    return results
