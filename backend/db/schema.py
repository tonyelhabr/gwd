from fastapi import FastAPI
from pydantic import BaseModel, Optional, AnyHttpUrl
import datetime

app = FastAPI("gwd")


class Venue(BaseModel):
    venue_id: float
    url: AnyHttpUrl
    lat: float
    lon: float
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class AdditionalVenueInfo(BaseModel):
    venue: Venue
    venue_link: AnyHttpUrl
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    updated_at: datetime.datetime

class QuizResults(BaseModel):
    venue_id: float
    quiz_date: str # something like 2022-W09
    team_name: str
    points: int
    rank: int