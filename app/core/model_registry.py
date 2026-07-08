from sqlalchemy.orm import Session
from app.models import Model
from app.utils.storage import StorageManager
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ModelRegistry:
    """Manages model versioning and registration"""

    @staticmethod
    def register_model(
        db: Session,
        machine_id: int,
        model_type: str,
        model_artifact: object,
        metrics: dict,
        hyperparameters: dict
    ) -> Model:
        """Register a new model in the registry"""
        
        # Generate model ID
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        model_name = f"{machine_id}_{model_type}_{timestamp}"
        
        # Save artifact
        artifact_path = StorageManager.save_artifact(model_artifact, model_name, "model")
        
        # Save metrics
        StorageManager.save_metrics(metrics, model_name)
        
        # Create model record
        model = Model(
            name=model_name,
            version="1.0.0",
            machine_id=machine_id,
            model_type=model_type,
            artifact_path=artifact_path,
            metrics=metrics,
            hyperparameters=hyperparameters,
            is_active=True
        )
        
        db.add(model)
        db.commit()
        db.refresh(model)
        
        logger.info(f"Model registered: {model_name} (ID: {model.id})")
        return model

    @staticmethod
    def get_active_model(db: Session, machine_id: int) -> Model:
        """Get the latest active model for a machine"""
        model = db.query(Model).filter(
            Model.machine_id == machine_id,
            Model.is_active == True
        ).order_by(Model.created_at.desc()).first()
        
        return model

    @staticmethod
    def deactivate_model(db: Session, model_id: int):
        """Deactivate a model"""
        model = db.query(Model).filter(Model.id == model_id).first()
        if model:
            model.is_active = False
            db.commit()
            logger.info(f"Model {model_id} deactivated")