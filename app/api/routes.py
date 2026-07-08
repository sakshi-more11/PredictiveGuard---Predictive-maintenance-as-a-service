from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api import ingest, train, predict, jobs, alerts

router = APIRouter(prefix="/api/v1", tags=["api"])

# Include route modules
router.include_router(ingest.router)
router.include_router(train.router)
router.include_router(predict.router)
router.include_router(jobs.router)
router.include_router(alerts.router)