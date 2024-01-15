from .database import Base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship, mapped_column


class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    results = relationship("Result", back_populates="venue")

    def __repr__(self):
        return "<Venue: {} ({})>".format(self.name, self.id)


class Result(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    venue_id: Mapped[int] = mapped_column(Integer, ForeignKey("venues.id"))
    team_name: Mapped[str] = mapped_column(String)
    rank: Mapped[int] = mapped_column(Integer)
    venue = relationship("Venue", back_populates="results")

    def __repr__(self):
        return "<Results: {}>".format(self.id)
