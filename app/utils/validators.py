import pandas as pd
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

def validate_csv_format(df: pd.DataFrame) -> Tuple[bool, str]:
    """Validate CSV has required columns"""
    required_columns = ['timestamp', 'temperature', 'vibration', 'pressure']
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False, f"Missing required columns: {missing_columns}"
    
    # Check for NaN values
    if df[required_columns].isnull().any().any():
        logger.warning("CSV contains NaN values in required columns")
    
    return True, "CSV format is valid"

def validate_timestamp(df: pd.DataFrame) -> Tuple[bool, str]:
    """Validate timestamp column"""
    try:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        if not df['timestamp'].is_monotonic_increasing:
            logger.warning("Timestamps are not in chronological order")
        return True, "Timestamps are valid"
    except Exception as e:
        return False, f"Timestamp validation failed: {str(e)}"

def validate_sensor_values(df: pd.DataFrame) -> Tuple[bool, str]:
    """Validate sensor values are within reasonable ranges"""
    sensor_ranges = {
        'temperature': (-50, 150),  # Celsius
        'vibration': (0, 1000),      # mm/s
        'pressure': (0, 1000),       # bar
    }
    
    for sensor, (min_val, max_val) in sensor_ranges.items():
        if sensor in df.columns:
            out_of_range = ((df[sensor] < min_val) | (df[sensor] > max_val)).sum()
            if out_of_range > 0:
                logger.warning(f"{sensor}: {out_of_range} values out of range [{min_val}, {max_val}]")
    
    return True, "Sensor values are valid"