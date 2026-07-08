from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from app.database import get_db
from app.models import Alert, Machine
from app.schemas import AlertCreate, AlertResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.post("/")
def create_alert(
    request: AlertCreate,
    db: Session = Depends(get_db)
) -> AlertResponse:
    """Create an alert configuration"""
    
    # Verify machine exists
    machine = db.query(Machine).filter(Machine.id == request.machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    alert = Alert(
        machine_id=request.machine_id,
        failure_probability_threshold=request.failure_probability_threshold,
        rul_threshold_days=request.rul_threshold_days,
        webhook_url=request.webhook_url,
        email_recipients=request.email_recipients
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    
    logger.info(f"Alert created: alert_id={alert.id}, machine_id={request.machine_id}")
    
    return AlertResponse.from_orm(alert)

@router.get("/machine/{machine_id}")
def get_machine_alerts(
    machine_id: int,
    db: Session = Depends(get_db)
):
    """Get all alerts for a machine"""
    
    alerts = db.query(Alert).filter(Alert.machine_id == machine_id).all()
    return [AlertResponse.from_orm(alert) for alert in alerts]

@router.put("/{alert_id}")
def update_alert(
    alert_id: int,
    request: AlertCreate,
    db: Session = Depends(get_db)
) -> AlertResponse:
    """Update alert configuration"""
    
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.failure_probability_threshold = request.failure_probability_threshold
    alert.rul_threshold_days = request.rul_threshold_days
    alert.webhook_url = request.webhook_url
    alert.email_recipients = request.email_recipients
    
    db.commit()
    db.refresh(alert)
    
    return AlertResponse.from_orm(alert)

@router.delete("/{alert_id}")
def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """Delete alert"""
    
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    db.delete(alert)
    db.commit()
    
    return {"detail": "Alert deleted"}