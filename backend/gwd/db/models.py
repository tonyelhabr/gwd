from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship


class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String)
    results = relationship("Result", back_populates="venue")

    def __repr__(self):
        return "<Venue: {} ({})>".format(self.name, self.id)


class Result(Base):
    __tablename__ = "results"

    id: Mapped[int] = Column(Integer, primary_key=True)
    venue_id: Mapped[int] = Column(Integer, ForeignKey("venues.id"))
    team_name: Mapped[str] = Column(String)
    rank: Mapped[int] = Column(Integer)
    venue = relationship("Venue", back_populates="results")

    def __repr__(self):
        return "<Results: {}>".format(self.id)
