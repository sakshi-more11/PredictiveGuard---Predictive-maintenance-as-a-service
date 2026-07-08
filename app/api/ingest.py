from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import logging
from app.database import get_db
from app.models import Machine, TrainingJob
from app.schemas import IngestResponse
from app.utils.storage import StorageManager
from app.utils.validators import (
    validate_csv_format, validate_timestamp, validate_sensor_values
)
from app.tasks.worker_tasks import preprocess_sensor_data

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ingest", tags=["ingest"])

@router.post("/upload")
async def upload_sensor_data(
    machine_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload sensor data CSV"""
    
    try:
        # Verify machine exists
        machine = db.query(Machine).filter(Machine.id == machine_id).first()
        if not machine:
            raise HTTPException(status_code=404, detail="Machine not found")
        
        # Read file
        contents = await file.read()
        df = pd.read_csv(pd.io.common.StringIO(contents.decode('utf-8')))
        
        # Validate CSV format
        valid, msg = validate_csv_format(df)
        if not valid:
            raise HTTPException(status_code=400, detail=msg)
        
        # Validate timestamps
        valid, msg = validate_timestamp(df)
        if not valid:
            raise HTTPException(status_code=400, detail=msg)
        
        # Validate sensor values
        valid, msg = validate_sensor_values(df)
        
        # Save raw file
        file_path = StorageManager.save_csv(df, f"machine_{machine_id}_raw.csv", "raw")
        
        # Enqueue preprocessing task
        task = preprocess_sensor_data.delay(machine_id, file_path)
        
        logger.info(f"Upload processed: machine_id={machine_id}, task_id={task.id}, rows={len(df)}")
        
        return IngestResponse(
            machine_id=machine_id,
            task_id=task.id,
            status="processing",
            message="Data uploaded and preprocessing started",
            rows_uploaded=len(df)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/machines")
def list_machines(db: Session = Depends(get_db)):
    """List all machines"""
    machines = db.query(Machine).all()
    return machines

@router.post("/machines")
def create_machine(
    name: str,
    machine_type: str,
    description: str = None,
    location: str = None,
    db: Session = Depends(get_db)
):
    """Create a new machine"""
    
    machine = Machine(
        name=name,
        machine_type=machine_type,
        description=description,
        location=location
    )
    db.add(machine)
    db.commit()
    db.refresh(machine)
    
    logger.info(f"Machine created: {machine.name} (ID: {machine.id})")
    return machine