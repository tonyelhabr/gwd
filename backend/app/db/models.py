from app.db.database import Base
from sqlalchemy import ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import Mapped, relationship, mapped_column
from datetime import datetime


class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_id: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    address: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    results = relationship("Result", back_populates="venue")

    def __repr__(self):
        return "<Venue: {} ({})>".format(self.name, self.id)


class Result(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_id: Mapped[int] = mapped_column(Integer, ForeignKey("venues.source_id"))
    quiz_date: Mapped[datetime] = mapped_column(DateTime)
    team_name: Mapped[str] = mapped_column(String)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True, default=False)
    score: Mapped[int] = mapped_column(Integer, nullable=True, default=False)
    venue = relationship("Venue", back_populates="results")

    def __repr__(self):
        return "<Results: {}>".format(self.id)
