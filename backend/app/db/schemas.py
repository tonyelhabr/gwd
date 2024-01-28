from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ResultBase(BaseModel):
    source_id: str
    team_name: str
    ranking: Optional[int] = None
    score: Optional[int] = None


class ResultUpdate(ResultBase):
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ResultCreate(ResultBase):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Result(ResultBase):
    id: int
    created_at: datetime
    updated_at: datetime

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
