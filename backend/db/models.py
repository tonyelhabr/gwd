from db.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, BigInteger, Integer, String, Float
from sqlalchemy.orm import Mapped
import datetime

class Venue(Base):
    __tablename__ = "venues"
    
    id: Mapped[int] = Column(BigInteger, primary_key=True, index=True)
    name: Mapped[str] = Column(String)
    address_line_1: Mapped[str] = Column(String)
    address_line_2: Mapped[str] = Column(String)
    city: Mapped[str] = Column(String)
    state: Mapped[str] = Column(String)
    
    created_at: Mapped[datetime.datetime] = Column(DateTime)
    updated_at: Mapped[datetime.datetime] = Column(DateTime)

    def __repr__(self):
        return "<Venue: {} ({})>".format(self.name, self.id)
  
class QuizResults(Base):
    __tablename__ = "quiz_results"
    
    id = Column(Integer, primary_key=True)
    venue_id = Column(BigInteger, ForeignKey("venues.id"))
    quiz_date = Column(String)
    team_name = Column(String, index=True)
    rank = Column(Integer)
    score = Column(Float)

    def __repr__(self):
        return "<Quiz results: {}>".format( self.id)
  