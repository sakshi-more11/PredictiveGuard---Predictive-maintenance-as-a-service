from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.config import settings
from app.database import init_db
from app.utils.logger import logger
from app.api.routes import router

# Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting PredictiveGuard API")
    init_db()
    yield
    # Shutdown
    logger.info("Shutting down PredictiveGuard API")

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.api_title,
        "version": settings.api_version
    }

@app.get("/")
def root():
    return {
        "service": settings.api_title,
        "version": settings.api_version,
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        workers=settings.workers
    )