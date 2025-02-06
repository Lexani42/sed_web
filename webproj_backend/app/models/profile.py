from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    source = Column(String, nullable=False)
    telegram_tag = Column(String)
    birth_date = Column(Date)
    
    hobbies = relationship("Hobby", back_populates="profile", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="profile", cascade="all, delete-orphan")

class Hobby(Base):
    __tablename__ = "hobbies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    
    profile = relationship("Profile", back_populates="hobbies")

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    
    profile = relationship("Profile", back_populates="notes")
