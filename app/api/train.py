from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from app.database import get_db
from app.models import Machine, TrainingJob
from app.schemas import TrainingJobCreate, TrainingJobResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/train", tags=["training"])

@router.post("/")
def start_training(
    request: TrainingJobCreate,
    db: Session = Depends(get_db)
) -> TrainingJobResponse:
    """Start a training job"""
    
    # Verify machine exists
    machine = db.query(Machine).filter(Machine.id == request.machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    # Create training job record
    training_job = TrainingJob(
        machine_id=request.machine_id,
        model_type=request.model_type,
        parameters=request.parameters,
        status="pending"
    )
    db.add(training_job)
    db.commit()
    db.refresh(training_job)
    
    # Enqueue task
    from app.tasks.worker_tasks import train_model

    task = train_model.delay(
        request.machine_id,
        request.model_type,
        training_job.id
    )
    
    # Update job with task ID
    training_job.celery_task_id = task.id
    db.commit()
    db.refresh(training_job)
    
    logger.info(f"Training job created: {training_job.id}, task_id={task.id}")
    
    return TrainingJobResponse.model_validate(training_job)

@router.get("/{job_id}")
def get_training_status(
    job_id: int,
    db: Session = Depends(get_db)
) -> TrainingJobResponse:
    """Get training job status"""
    
    job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Training job not found")
    
    return TrainingJobResponse.model_validate(job)
