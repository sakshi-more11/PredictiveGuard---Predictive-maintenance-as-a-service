import pandas as pd
import logging
from celery import states
from app.tasks.celery_app import celery_app
from app.database import SessionLocal
from app.models import TrainingJob, SensorReading, TrainingJobStatus
from app.core.preprocessing import DataPreprocessor
from app.core.training import ModelTrainer
from app.core.model_registry import ModelRegistry
from app.utils.storage import StorageManager
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def preprocess_sensor_data(self, machine_id: int, file_path: str):
    """Preprocess uploaded sensor data"""
    
    try:
        self.update_state(state='PROCESSING', meta={'current': 0, 'total': 3})
        
        # Load CSV
        df = pd.read_csv(file_path)
        logger.info(f"Loaded CSV: {df.shape}")
        
        # Preprocess
        self.update_state(state='PROCESSING', meta={'current': 1, 'total': 3})
        df = DataPreprocessor.preprocess_data(df, machine_id)
        
        # Engineer features
        self.update_state(state='PROCESSING', meta={'current': 2, 'total': 3})
        df = DataPreprocessor.engineer_features(df)
        
        # Save processed data
        processed_path = StorageManager.save_csv(df, f"machine_{machine_id}_processed.csv", "processed")
        
        self.update_state(state='PROCESSING', meta={'current': 3, 'total': 3})
        
        return {
            "status": "success",
            "machine_id": machine_id,
            "processed_path": processed_path,
            "rows": len(df)
        }
        
    except Exception as e:
        logger.error(f"Preprocessing failed: {str(e)}")
        self.update_state(state=states.FAILURE, meta={'error': str(e)})
        raise

@celery_app.task(bind=True)
def train_model(self, machine_id: int, model_type: str = "prophet", training_job_id: int = None):
    """Train model for a machine"""
    
    db = SessionLocal()
    
    try:
        # Update job status
        if training_job_id:
            job = db.query(TrainingJob).filter(TrainingJob.id == training_job_id).first()
            if job:
                job.status = TrainingJobStatus.RUNNING.value
                job.started_at = pd.Timestamp.utcnow()
                db.commit()
        
        self.update_state(state='TRAINING', meta={'current': 0, 'total': 5})
        
        # Load processed data
        df = pd.read_csv(f"./data/processed/machine_{machine_id}_processed.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        self.update_state(state='TRAINING', meta={'current': 1, 'total': 5})
        
        # Normalize data
        df, norm_params = DataPreprocessor.normalize_data(df)
        
        # Train model based on type
        self.update_state(state='TRAINING', meta={'current': 2, 'total': 5})
        
        if model_type == "prophet":
            model, metrics = ModelTrainer.train_prophet_model(df, machine_id)
        else:
            model, metrics = ModelTrainer.train_simple_degradation_model(df, machine_id)
        
        self.update_state(state='TRAINING', meta={'current': 3, 'total': 5})
        
        # Register model
        hyperparams = {"model_type": model_type, "normalization": norm_params}
        registered_model = ModelRegistry.register_model(
            db,
            machine_id,
            model_type,
            model,
            metrics,
            hyperparams
        )
        
        self.update_state(state='TRAINING', meta={'current': 4, 'total': 5})
        
        # Update job
        if training_job_id:
            job = db.query(TrainingJob).filter(TrainingJob.id == training_job_id).first()
            if job:
                job.status = TrainingJobStatus.COMPLETED.value
                job.completed_at = pd.Timestamp.utcnow()
                job.model_id = registered_model.id
                db.commit()
        
        self.update_state(state='TRAINING', meta={'current': 5, 'total': 5})
        
        logger.info(f"Model training completed: model_id={registered_model.id}")
        
        return {
            "status": "success",
            "model_id": registered_model.id,
            "model_type": model_type,
            "metrics": metrics
        }
        
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        
        if training_job_id:
            job = db.query(TrainingJob).filter(TrainingJob.id == training_job_id).first()
            if job:
                job.status = TrainingJobStatus.FAILED.value
                job.error_message = str(e)
                db.commit()
        
        self.update_state(state=states.FAILURE, meta={'error': str(e)})
        raise
        
    finally:
        db.close()

@celery_app.task
def check_alerts():
    """Scheduled task to check alerts and trigger notifications"""
    db = SessionLocal()
    
    try:
        from app.models import Alert, Prediction
        from app.core.alerting import AlertingService
        
        # Get recent predictions
        recent_predictions = db.query(Prediction).order_by(Prediction.created_at.desc()).limit(100).all()
        
        for prediction in recent_predictions:
            # Get associated alerts
            alerts = db.query(Alert).filter(Alert.machine_id == prediction.machine_id).all()
            
            for alert in alerts:
                AlertingService.trigger_alert(
                    db,
                    alert,
                    prediction.id,
                    prediction.rul_estimate,
                    prediction.failure_probability
                )
        
        logger.info(f"Alert check completed. Checked {len(recent_predictions)} predictions")
        
    except Exception as e:
        logger.error(f"Alert check failed: {str(e)}")
        
    finally:
        db.close()