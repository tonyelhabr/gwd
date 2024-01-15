from pydantic import BaseModel


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
    name: str


class VenueCreate(VenueBase):
    pass


class Venue(VenueBase):
    id: int
    results: list[Result] = []

    class Config:
        from_attributes = True
