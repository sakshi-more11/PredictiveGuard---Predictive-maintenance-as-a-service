import requests
import logging
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Alert, AlertLog
from app.config import settings

logger = logging.getLogger(__name__)

class AlertingService:
    """Manages alert notifications and webhooks"""

    @staticmethod
    def trigger_alert(
        db: Session,
        alert: Alert,
        prediction_id: int,
        rul_estimate: float,
        failure_probability: float
    ):
        """Trigger alert if thresholds are exceeded"""
        
        # Check thresholds
        should_alert = (
            failure_probability > alert.failure_probability_threshold or
            rul_estimate < alert.rul_threshold_days
        )
        
        if not should_alert:
            return
        
        # Send webhook
        if alert.webhook_url:
            AlertingService.send_webhook(
                db, alert, prediction_id, rul_estimate, failure_probability
            )
        
        # Send emails
        if alert.email_recipients:
            AlertingService.send_emails(
                alert, prediction_id, rul_estimate, failure_probability
            )

    @staticmethod
    def send_webhook(
        db: Session,
        alert: Alert,
        prediction_id: int,
        rul_estimate: float,
        failure_probability: float
    ):
        """Send webhook notification"""
        
        payload = {
            "alert_id": alert.id,
            "machine_id": alert.machine_id,
            "prediction_id": prediction_id,
            "rul_estimate": rul_estimate,
            "failure_probability": failure_probability,
            "timestamp": datetime.utcnow().isoformat(),
            "message": f"RUL: {rul_estimate:.1f} days, Failure probability: {failure_probability:.2%}"
        }
        
        try:
            response = requests.post(
                alert.webhook_url,
                json=payload,
                timeout=settings.webhook_timeout
            )
            status_code = response.status_code
            response_body = response.text
            
        except Exception as e:
            logger.error(f"Webhook failed: {str(e)}")
            status_code = None
            response_body = str(e)
        
        # Log alert
        alert_log = AlertLog(
            alert_id=alert.id,
            machine_id=alert.machine_id,
            prediction_id=prediction_id,
            webhook_response_status=status_code,
            webhook_response_body=response_body
        )
        db.add(alert_log)
        db.commit()
        
        logger.info(f"Webhook sent for alert {alert.id}, status: {status_code}")

    @staticmethod
    def send_emails(
        alert: Alert,
        prediction_id: int,
        rul_estimate: float,
        failure_probability: float
    ):
        """Send email notifications (mock implementation)"""
        logger.info(f"Email alert would be sent to: {alert.email_recipients}")