import os
import json
import pickle
from pathlib import Path
from typing import Any, Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class StorageManager:
    """Manages local and remote storage of artifacts and data"""

    @staticmethod
    def save_artifact(artifact: Any, artifact_id: str, artifact_type: str = "model") -> str:
        """Save model artifact locally or to MinIO"""
        path = Path(settings.artifact_storage_path) / artifact_type / f"{artifact_id}.pkl"
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'wb') as f:
            pickle.dump(artifact, f)
        
        logger.info(f"Artifact saved: {path}")
        return str(path)

    @staticmethod
    def load_artifact(artifact_id: str, artifact_type: str = "model") -> Any:
        """Load model artifact from local storage or MinIO"""
        path = Path(settings.artifact_storage_path) / artifact_type / f"{artifact_id}.pkl"
        
        if not path.exists():
            logger.error(f"Artifact not found: {path}")
            return None
        
        with open(path, 'rb') as f:
            artifact = pickle.load(f)
        
        return artifact

    @staticmethod
    def save_metrics(metrics: dict, model_id: str) -> str:
        """Save model metrics as JSON"""
        path = Path(settings.metrics_storage_path) / f"{model_id}_metrics.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        logger.info(f"Metrics saved: {path}")
        return str(path)

    @staticmethod
    def load_metrics(model_id: str) -> Optional[dict]:
        """Load model metrics from JSON"""
        path = Path(settings.metrics_storage_path) / f"{model_id}_metrics.json"
        
        if not path.exists():
            return None
        
        with open(path, 'r') as f:
            metrics = json.load(f)
        
        return metrics

    @staticmethod
    def save_csv(data: Any, filename: str, folder: str = "raw") -> str:
        """Save CSV data"""
        path = Path(settings.upload_folder) / folder / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        data.to_csv(path, index=False)
        logger.info(f"CSV saved: {path}")
        return str(path)