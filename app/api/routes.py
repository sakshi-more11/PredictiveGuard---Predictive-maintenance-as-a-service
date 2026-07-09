from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api import ingest, train, predict, jobs, alerts
from app.config import settings
from app.models import Alert, Machine, Model, Prediction

router = APIRouter(prefix="/api/v1", tags=["api"])

# Include route modules
router.include_router(ingest.router)
router.include_router(train.router)
router.include_router(predict.router)
router.include_router(jobs.router)
router.include_router(alerts.router)

@router.get("/dashboard")
def dashboard_summary(db: Session = Depends(get_db)):
    """Return summary data used by the React dashboard and analytics pages."""
    machines = db.query(Machine).all()
    latest_predictions = (
        db.query(Prediction, Machine)
        .join(Machine, Prediction.machine_id == Machine.id)
        .order_by(Prediction.created_at.desc())
        .limit(10)
        .all()
    )
    active_alerts = (
        db.query(Alert, Machine)
        .join(Machine, Alert.machine_id == Machine.id)
        .filter(Alert.is_active == True)
        .order_by(Alert.created_at.desc())
        .limit(10)
        .all()
    )

    prediction_rows = [prediction for prediction, _machine in latest_predictions]
    average_rul = (
        sum(prediction.rul_estimate for prediction in prediction_rows) / len(prediction_rows)
        if prediction_rows
        else 0
    )
    high_risk_assets = len(
        [prediction for prediction in prediction_rows if prediction.failure_probability >= 0.7]
    )
    fleet_health = max(0, round(100 - (high_risk_assets / max(len(machines), 1) * 100)))

    return {
        "monitored_assets": len(machines),
        "fleet_health": fleet_health,
        "high_risk_assets": high_risk_assets,
        "average_rul_days": round(average_rul, 1),
        "latest_predictions": [
            {
                "id": prediction.id,
                "machine_id": prediction.machine_id,
                "machine_name": machine.name,
                "rul_estimate": prediction.rul_estimate,
                "failure_probability": prediction.failure_probability,
                "created_at": prediction.created_at,
            }
            for prediction, machine in latest_predictions
        ],
        "active_alerts": [
            {
                "id": alert.id,
                "machine_id": alert.machine_id,
                "machine_name": machine.name,
                "failure_probability_threshold": alert.failure_probability_threshold,
                "rul_threshold_days": alert.rul_threshold_days,
                "is_active": alert.is_active,
            }
            for alert, machine in active_alerts
        ],
    }

@router.get("/models")
def list_models(db: Session = Depends(get_db)):
    """Return registered model metadata."""
    return db.query(Model).order_by(Model.created_at.desc()).all()

@router.get("/settings")
def runtime_settings():
    """Return non-secret runtime settings for the UI."""
    return {
        "api_title": settings.api_title,
        "api_version": settings.api_version,
        "debug": settings.debug,
        "storage_type": settings.storage_type,
    }
