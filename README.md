# PredictiveGuard - Predictive Maintenance as a Service

An AI-powered predictive maintenance platform that predicts Remaining Useful Life (RUL), estimates failure risk, and automates maintenance alerts using FastAPI, Celery, Redis, PostgreSQL, MinIO, and Docker Compose.

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sakshi-more11/PredictiveGuard---Predictive-maintenance-as-a-service.git
   cd PredictiveGuard---Predictive-maintenance-as-a-service
   ```

2. **Copy environment file**
   ```bash
   cp .env.example .env
   ```

3. **Start services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Initialize database**
   ```bash
   docker-compose exec api python -c "from app.database import init_db; init_db()"
   ```

5. **Access the API**
   - API Docs: http://localhost:8000/docs
   - MinIO Console: http://localhost:9001 (minioadmin/minioadmin)

## Features

- **Sensor Data Ingestion**: Upload CSV or stream sensor data (temperature, vibration, pressure, etc.)
- **Model Training**: Asynchronous training with Prophet, DeepAR, or custom models
- **RUL Prediction**: Estimate Remaining Useful Life with confidence intervals
- **Failure Probability**: Predict failure likelihood within configurable horizons
- **Automated Alerts**: Webhook notifications and email alerts based on thresholds
- **Model Registry**: Version control and lifecycle management for trained models
- **Scheduled Retraining**: Automatic model retraining with cron or event-triggered jobs
- **Monitoring**: Prometheus metrics, structured JSON logging, Sentry error tracking

## API Endpoints

### Machines
- `POST /api/v1/ingest/machines` - Create a machine
- `GET /api/v1/ingest/machines` - List all machines

### Data Ingestion
- `POST /api/v1/ingest/upload` - Upload sensor data CSV

### Training
- `POST /api/v1/train/` - Start training job
- `GET /api/v1/train/{job_id}` - Get training status

### Predictions
- `POST /api/v1/predict/` - Make a prediction
- `GET /api/v1/predict/machine/{machine_id}` - Get latest prediction

### Alerts
- `POST /api/v1/alerts/` - Create alert configuration
- `GET /api/v1/alerts/machine/{machine_id}` - List alerts for machine
- `PUT /api/v1/alerts/{alert_id}` - Update alert
- `DELETE /api/v1/alerts/{alert_id}` - Delete alert

### Jobs
- `GET /api/v1/jobs/{job_id}` - Get job status
- `GET /api/v1/jobs/machine/{machine_id}` - Get machine's jobs

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│   FastAPI (app/api)                 │
│   - Routes & Endpoints              │
│   - Request Validation              │
└──────┬──────────────────────────────┘
       │
       ├──────────────────────┬──────────────────────┐
       ▼                      ▼                      ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  PostgreSQL  │     │  Redis       │     │   MinIO      │
│  (Metadata)  │     │  (Cache)     │     │  (Storage)   │
└──────────────┘     └──────────────┘     └──────────────┘
                            ▲
                            │
       ┌────────────────────┼────────────────────┐
       ▼                    ▼                    ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Celery Worker   │ │ Celery Worker   │ │  Celery Beat    │
│ (Training)      │ │ (Inference)     │ │  (Scheduling)   │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## Development

### Local Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run API server**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Run Celery worker**
   ```bash
   celery -A app.tasks.celery_app worker --loglevel=info
   ```

5. **Run Celery Beat**
   ```bash
   celery -A app.tasks.celery_app beat --loglevel=info
   ```

### Running Tests

```bash
pytest tests/ -v --cov=app
```

