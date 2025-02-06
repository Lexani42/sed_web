from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Opener(Base):
    __tablename__ = "openers"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    context = Column(String, nullable=False)
    
    continue_options = relationship("ContinueOption", back_populates="opener", cascade="all, delete-orphan")

class ContinueOption(Base):
    __tablename__ = "continue_options"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    weight = Column(Float, nullable=False, default=1.0)
    opener_id = Column(Integer, ForeignKey("openers.id"), nullable=False)
    
    opener = relationship("Opener", back_populates="continue_options")
