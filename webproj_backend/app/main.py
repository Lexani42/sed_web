from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import dialogs_router, profiles_router, stories_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue.js default dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dialogs_router, prefix=f"{settings.API_V1_STR}/dialogs", tags=["dialogs"])
app.include_router(profiles_router, prefix=f"{settings.API_V1_STR}/profiles", tags=["profiles"])
app.include_router(stories_router, prefix=f"{settings.API_V1_STR}/stories", tags=["stories"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Story Manager API",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }
