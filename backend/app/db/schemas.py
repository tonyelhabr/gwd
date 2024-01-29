from pydantic import BaseModel, Field, computed_field
from datetime import datetime, date
from typing import Optional


class ISOWeek(BaseModel):
    @classmethod
    def from_date(cls, date: date):
        iso_year, iso_week, _ = date.isocalendar()
        return f"{iso_year}-W{iso_week:02d}"


class ResultBase(BaseModel):
    source_id: str
    quiz_date: date
    team_name: str
    ranking: Optional[int] = None
    score: Optional[int] = None


class ResultUpdate(ResultBase):
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ResultCreate(ResultBase):
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @computed_field
    @property
    def quiz_week(self) -> str:
        return ISOWeek.from_date(self.quiz_date)


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
