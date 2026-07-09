from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import logging
from app.database import get_db
from app.models import Machine, Prediction, SensorReading
from app.schemas import PredictionRequest, PredictionResponse
from app.core.model_registry import ModelRegistry
from app.core.prediction import PredictionEngine
from app.utils.storage import StorageManager
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/predict", tags=["prediction"])

@router.get("/")
def list_predictions(db: Session = Depends(get_db)):
    """Get recent predictions"""
    predictions = db.query(Prediction).order_by(Prediction.created_at.desc()).limit(100).all()
    return [PredictionResponse.model_validate(prediction) for prediction in predictions]

@router.post("/")
def make_prediction(
    request: PredictionRequest,
    db: Session = Depends(get_db)
) -> PredictionResponse:
    """Make a prediction for a machine"""
    
    # Verify machine exists
    machine = db.query(Machine).filter(Machine.id == request.machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    # Get latest model
    model = ModelRegistry.get_active_model(db, request.machine_id)
    if not model:
        raise HTTPException(status_code=404, detail="No trained model found for this machine")
    
    try:
        # Load model artifact
        model_artifact = StorageManager.load_artifact(model.name, "model")
        if not model_artifact:
            raise HTTPException(status_code=404, detail="Model artifact not found")
        
        # Get latest sensor data
        sensor_data = db.query(SensorReading).filter(
            SensorReading.machine_id == request.machine_id
        ).order_by(SensorReading.timestamp.desc()).limit(100).all()
        
        if not sensor_data:
            raise HTTPException(status_code=404, detail="No sensor data found")
        
        # Convert to DataFrame
        df = pd.DataFrame([
            {
                "timestamp": s.timestamp,
                "temperature": s.temperature,
                "vibration": s.vibration,
                "pressure": s.pressure,
            }
            for s in reversed(sensor_data)
        ])
        
        # Make prediction
        prediction_result = PredictionEngine.predict_rul(
            model_artifact,
            df,
            request.horizon_days
        )
        
        # Store prediction
        prediction = Prediction(
            machine_id=request.machine_id,
            model_id=model.id,
            rul_estimate=prediction_result["rul_estimate"],
            failure_probability=prediction_result["failure_probability"],
            lower_confidence_interval=prediction_result["lower_confidence_interval"],
            upper_confidence_interval=prediction_result["upper_confidence_interval"],
            confidence_level=prediction_result["confidence_level"],
            top_features=prediction_result["top_features"],
            prediction_horizon_days=request.horizon_days
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        
        logger.info(f"Prediction made: machine_id={request.machine_id}, rul={prediction_result['rul_estimate']}")
        
        return PredictionResponse.model_validate(prediction)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/machine/{machine_id}")
def get_latest_prediction(
    machine_id: int,
    db: Session = Depends(get_db)
) -> PredictionResponse:
    """Get latest prediction for a machine"""
    
    prediction = db.query(Prediction).filter(
        Prediction.machine_id == machine_id
    ).order_by(Prediction.created_at.desc()).first()
    
    if not prediction:
        raise HTTPException(status_code=404, detail="No predictions found")
    
    return PredictionResponse.model_validate(prediction)
