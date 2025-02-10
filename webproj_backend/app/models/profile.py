from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from app.core.config import settings

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    source = Column(String, nullable=False)
    telegram_tag = Column(String)
    birth_date = Column(Date)
    photo = Column(String, default="/static/avatars/avatar.jpg")
    
    # Relations
    opener_id = Column(Integer, ForeignKey("openers.id"))
    story_id = Column(Integer, ForeignKey("stories.id"))
    
    # Checkpoints
    answered_opener = Column(Boolean, default=False)
    story_discussed = Column(Boolean, default=False)
    closed_for_meet = Column(Boolean, default=False)
    closed_for_sex = Column(Boolean, default=False)
    
    # Relationships
    hobbies = relationship("Hobby", back_populates="profile", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="profile", cascade="all, delete-orphan")
    opener = relationship("Opener", backref="profiles")
    story = relationship("Story", backref="profiles")

    @property
    def photo_url(self):
        if self.photo.startswith('http'):
            return self.photo
        return f"{settings.BACKEND_URL}{self.photo}"

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
