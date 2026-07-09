from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from app.database import get_db
from app.models import TrainingJob
from app.schemas import TrainingJobResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/")
def list_jobs(db: Session = Depends(get_db)):
    """Get all jobs"""
    jobs = db.query(TrainingJob).order_by(TrainingJob.created_at.desc()).all()
    return [TrainingJobResponse.model_validate(job) for job in jobs]

@router.get("/{job_id}")
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db)
):
    """Get job status"""
    
    job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Get Celery task status
    if job.celery_task_id:
        from app.tasks.celery_app import celery_app

        celery_task = celery_app.AsyncResult(job.celery_task_id)
        task_status = celery_task.status
        task_result = celery_task.result if celery_task.successful() else None
    else:
        task_status = None
        task_result = None
    
    return {
        "job_id": job.id,
        "machine_id": job.machine_id,
        "model_type": job.model_type,
        "status": job.status,
        "celery_status": task_status,
        "started_at": job.started_at,
        "completed_at": job.completed_at,
        "model_id": job.model_id,
        "error_message": job.error_message,
        "result": task_result
    }

@router.get("/machine/{machine_id}")
def get_machine_jobs(
    machine_id: int,
    db: Session = Depends(get_db)
):
    """Get all jobs for a machine"""
    
    jobs = db.query(TrainingJob).filter(
        TrainingJob.machine_id == machine_id
    ).order_by(TrainingJob.created_at.desc()).all()
    
    return [TrainingJobResponse.model_validate(job) for job in jobs]
