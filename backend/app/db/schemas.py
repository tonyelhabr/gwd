from pydantic import BaseModel
from datetime import datetime


class ResultBase(BaseModel):
    team_name: str
    rank: int


class ResultCreate(ResultBase):
    pass


class Result(ResultBase):
    id: int
    venue_id: int

    class Config:
        from_attributes = True


class VenueBase(BaseModel):
    source_id: str
    name: str
    url: str
    lat: str
    lon: str
    address: str
    created_at: datetime
    updated_at: datetime


class VenueCreate(VenueBase):
    pass


class Venue(VenueBase):
    id: int
    results: list[Result] = []

    class Config:
        from_attributes = True
