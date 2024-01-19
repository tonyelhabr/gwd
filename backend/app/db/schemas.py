from pydantic import BaseModel, Field
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
    lat: float
    lon: float
    address: str


class VenueUpdate(VenueBase):
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class VenueCreate(VenueUpdate):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Venue(VenueBase):
    id: int
    created_at: datetime
    updated_at: datetime
    results: list[Result] = []

    class Config:
        from_attributes = True
