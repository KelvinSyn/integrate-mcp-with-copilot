"""
Database models for activities and participants
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base


class Activity(Base):
    """Activity model representing extracurricular activities"""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    schedule = Column(String, nullable=False)
    max_participants = Column(Integer, nullable=False)

    # Relationship to participants
    participants = relationship("Participant", back_populates="activity", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert activity to dictionary format matching the original API response"""
        return {
            "description": self.description,
            "schedule": self.schedule,
            "max_participants": self.max_participants,
            "participants": [p.email for p in self.participants]
        }


class Participant(Base):
    """Participant model representing students signed up for activities"""
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)

    # Relationship to activity
    activity = relationship("Activity", back_populates="participants")
