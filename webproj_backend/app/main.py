from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.db_init import init_db
from app.api.endpoints import dialogs_router, profiles_router, stories_router
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Initialize database
init_db()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://raspberrypi:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(dialogs_router, prefix=f"{settings.API_V1_STR}/openers", tags=["dialogs"])
app.include_router(profiles_router, prefix=f"{settings.API_V1_STR}/profiles", tags=["profiles"])
app.include_router(stories_router, prefix=f"{settings.API_V1_STR}/stories", tags=["stories"])

# Add after app initialization
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Story Manager API",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }
