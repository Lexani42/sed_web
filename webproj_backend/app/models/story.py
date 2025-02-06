from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Association tables for many-to-many relationships
story_formats = Table(
    'story_formats',
    Base.metadata,
    Column('story_id', Integer, ForeignKey('stories.id'), primary_key=True),
    Column('format_id', Integer, ForeignKey('formats.id'), primary_key=True)
)

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    
    languages = relationship("Language", back_populates="story", cascade="all, delete-orphan")
    formats = relationship("Format", secondary=story_formats, back_populates="stories")

class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(2), nullable=False)  # e.g., 'en', 'es'
    story_id = Column(Integer, ForeignKey("stories.id"), nullable=False)
    
    story = relationship("Story", back_populates="languages")
    contents = relationship("Content", back_populates="language", cascade="all, delete-orphan")

class Format(Base):
    __tablename__ = "formats"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)  # 'text' or 'audio'
    
    stories = relationship("Story", secondary=story_formats, back_populates="formats")
    contents = relationship("Content", back_populates="format", cascade="all, delete-orphan")

class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)  # For audio, this will be the file path
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    format_id = Column(Integer, ForeignKey("formats.id"), nullable=False)
    
    language = relationship("Language", back_populates="contents")
    format = relationship("Format", back_populates="contents")
