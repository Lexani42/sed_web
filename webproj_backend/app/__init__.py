from app.core.config import settings
from app.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)
