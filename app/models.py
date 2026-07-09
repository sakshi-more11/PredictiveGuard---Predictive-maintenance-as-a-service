from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    machine_type = Column(String(255), index=True)
    description = Column(String(500), nullable=True)
    location = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sensor_readings = relationship("SensorReading", back_populates="machine", cascade="all, delete-orphan")
    training_jobs = relationship("TrainingJob", back_populates="machine", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="machine", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="machine", cascade="all, delete-orphan")

    models = relationship("Model", back_populates="machine", cascade="all, delete-orphan")

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), index=True)
    timestamp = Column(DateTime, index=True)
    temperature = Column(Float)
    vibration = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float, nullable=True)
    power_consumption = Column(Float, nullable=True)
    rpm = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    machine = relationship("Machine", back_populates="sensor_readings")

class TrainingJobStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class TrainingJob(Base):
    __tablename__ = "training_jobs"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), index=True)
    celery_task_id = Column(String(255), unique=True, index=True)
    model_type = Column(String(50))  # prophet, deepar, tft
    status = Column(String(20), default=TrainingJobStatus.PENDING.value, index=True)
    parameters = Column(JSON, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    machine = relationship("Machine", back_populates="training_jobs")
    model = relationship("Model", back_populates="training_jobs")

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    version = Column(String(50))
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=True)
    model_type = Column(String(50))  # prophet, deepar, tft
    artifact_path = Column(String(500))
    metrics = Column(JSON, nullable=True)
    hyperparameters = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    machine = relationship("Machine", back_populates="models")
    training_jobs = relationship("TrainingJob", back_populates="model")
    predictions = relationship("Prediction", back_populates="model")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), index=True)
    model_id = Column(Integer, ForeignKey("models.id"))
    rul_estimate = Column(Float)  # Remaining Useful Life in days
    failure_probability = Column(Float)  # Probability in next horizon
    lower_confidence_interval = Column(Float)
    upper_confidence_interval = Column(Float)
    confidence_level = Column(Float)  # e.g., 0.80 for 80%
    top_features = Column(JSON, nullable=True)  # List of influential sensors
    prediction_horizon_days = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    machine = relationship("Machine", back_populates="predictions")
    model = relationship("Model", back_populates="predictions")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), index=True)
    failure_probability_threshold = Column(Float)  # Alert if prob > threshold
    rul_threshold_days = Column(Float)  # Alert if RUL < threshold
    webhook_url = Column(String(500), nullable=True)
    email_recipients = Column(JSON, nullable=True)  # List of emails
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    machine = relationship("Machine", back_populates="alerts")

class AlertLog(Base):
    __tablename__ = "alert_logs"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"), index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), index=True)
    prediction_id = Column(Integer, ForeignKey("predictions.id"), nullable=True)
    triggered_at = Column(DateTime, default=datetime.utcnow)
    webhook_response_status = Column(Integer, nullable=True)
    webhook_response_body = Column(Text, nullable=True)
    email_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)