from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Machine Schemas
class MachineBase(BaseModel):
    name: str
    machine_type: str
    description: Optional[str] = None
    location: Optional[str] = None

class MachineCreate(MachineBase):
    pass

class MachineUpdate(BaseModel):
    description: Optional[str] = None
    location: Optional[str] = None

class Machine(MachineBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Sensor Reading Schemas
class SensorReadingBase(BaseModel):
    temperature: float
    vibration: float
    pressure: float
    humidity: Optional[float] = None
    power_consumption: Optional[float] = None
    rpm: Optional[float] = None

class SensorReadingCreate(SensorReadingBase):
    machine_id: int
    timestamp: datetime

class SensorReading(SensorReadingBase):
    id: int
    machine_id: int
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True

# Training Job Schemas
class TrainingJobCreate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    machine_id: int
    model_type: str  # "prophet", "deepar", "tft"
    parameters: Optional[Dict[str, Any]] = None

class TrainingJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    id: int
    machine_id: int
    celery_task_id: Optional[str] = None
    model_type: str
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    model_id: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime

class TrainingJobStatus(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    id: int
    celery_task_id: str
    status: str
    model_id: Optional[int] = None
    error_message: Optional[str] = None
    progress: Optional[float] = None

# Model Schemas
class ModelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    id: int
    name: str
    version: str
    model_type: str
    metrics: Optional[Dict[str, Any]] = None
    hyperparameters: Optional[Dict[str, Any]] = None
    is_active: bool
    created_at: datetime

# Prediction Schemas
class PredictionRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    machine_id: int
    horizon_days: int = Field(30, ge=1, le=365)

class PredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    id: int
    machine_id: int
    model_id: int
    rul_estimate: float
    failure_probability: float
    lower_confidence_interval: float
    upper_confidence_interval: float
    confidence_level: float
    top_features: Optional[List[Dict[str, float]]] = None
    prediction_horizon_days: int
    created_at: datetime

# Alert Schemas
class AlertCreate(BaseModel):
    machine_id: int
    failure_probability_threshold: float = Field(0.7, ge=0, le=1)
    rul_threshold_days: float = Field(7, ge=1)
    webhook_url: Optional[str] = None
    email_recipients: Optional[List[str]] = None

class AlertResponse(BaseModel):
    id: int
    machine_id: int
    failure_probability_threshold: float
    rul_threshold_days: float
    webhook_url: Optional[str] = None
    email_recipients: Optional[List[str]] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Ingest Schemas
class IngestResponse(BaseModel):
    machine_id: int
    task_id: str
    status: str
    message: str
    rows_uploaded: int
