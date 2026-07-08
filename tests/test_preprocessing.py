import pytest
import pandas as pd
from app.core.preprocessing import DataPreprocessor

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'timestamp': pd.date_range('2024-01-01', periods=100, freq='H'),
        'temperature': [70 + i*0.1 for i in range(100)],
        'vibration': [5 + i*0.05 for i in range(100)],
        'pressure': [100 + i*0.02 for i in range(100)]
    })

def test_preprocess_data(sample_data):
    result = DataPreprocessor.preprocess_data(sample_data, machine_id=1)
    assert result is not None
    assert len(result) > 0
    assert 'machine_id' in result.columns

def test_engineer_features(sample_data):
    df = DataPreprocessor.preprocess_data(sample_data, 1)
    result = DataPreprocessor.engineer_features(df)
    assert len(result) < len(df)  # Some rows removed due to NaN
    assert 'temperature_lag_1' in result.columns