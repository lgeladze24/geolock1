from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..base import Base

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    description = Column(String)
    image_url = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    difficulty = Column(String)  # 'easy', 'medium', 'hard'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    creator = relationship("User", back_populates="challenges")
    guesses = relationship("Guess", back_populates="challenge")

class Guess(Base):
    __tablename__ = "guesses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    guessed_latitude = Column(Float)
    guessed_longitude = Column(Float)
    distance = Column(Float)  # Distance in kilometers
    score = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="guesses")
    challenge = relationship("Challenge", back_populates="guesses")