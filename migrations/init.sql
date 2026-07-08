-- Create tables
CREATE TABLE IF NOT EXISTS machines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    machine_type VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sensor_readings (
    id SERIAL PRIMARY KEY,
    machine_id INTEGER NOT NULL REFERENCES machines(id) ON DELETE CASCADE,
    timestamp TIMESTAMP NOT NULL,
    temperature FLOAT NOT NULL,
    vibration FLOAT NOT NULL,
    pressure FLOAT NOT NULL,
    humidity FLOAT,
    power_consumption FLOAT,
    rpm FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS training_jobs (
    id SERIAL PRIMARY KEY,
    machine_id INTEGER NOT NULL REFERENCES machines(id) ON DELETE CASCADE,
    celery_task_id VARCHAR(255) UNIQUE,
    model_type VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',
    parameters JSONB,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    model_id INTEGER,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    version VARCHAR(50),
    machine_id INTEGER REFERENCES machines(id),
    model_type VARCHAR(50),
    artifact_path VARCHAR(500),
    metrics JSONB,
    hyperparameters JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    machine_id INTEGER NOT NULL REFERENCES machines(id) ON DELETE CASCADE,
    model_id INTEGER NOT NULL REFERENCES models(id),
    rul_estimate FLOAT,
    failure_probability FLOAT,
    lower_confidence_interval FLOAT,
    upper_confidence_interval FLOAT,
    confidence_level FLOAT,
    top_features JSONB,
    prediction_horizon_days INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    machine_id INTEGER NOT NULL REFERENCES machines(id) ON DELETE CASCADE,
    failure_probability_threshold FLOAT,
    rul_threshold_days FLOAT,
    webhook_url VARCHAR(500),
    email_recipients JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alert_logs (
    id SERIAL PRIMARY KEY,
    alert_id INTEGER NOT NULL REFERENCES alerts(id),
    machine_id INTEGER NOT NULL REFERENCES machines(id),
    prediction_id INTEGER REFERENCES predictions(id),
    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    webhook_response_status INTEGER,
    webhook_response_body TEXT,
    email_sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_machines_type ON machines(machine_type);
CREATE INDEX idx_sensor_readings_machine_timestamp ON sensor_readings(machine_id, timestamp);
CREATE INDEX idx_training_jobs_status ON training_jobs(status);
CREATE INDEX idx_predictions_machine_created ON predictions(machine_id, created_at DESC);
CREATE INDEX idx_alerts_machine ON alerts(machine_id);