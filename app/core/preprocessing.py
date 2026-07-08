import pandas as pd
import numpy as np
from typing import Tuple, List
import logging

logger = logging.getLogger(__name__)

class DataPreprocessor:
    """Handles data preprocessing and feature engineering"""

    @staticmethod
    def preprocess_data(df: pd.DataFrame, machine_id: int) -> pd.DataFrame:
        """Main preprocessing pipeline"""
        df = df.copy()
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # Handle missing values
        df = DataPreprocessor.handle_missing_values(df)
        
        # Add machine_id
        df['machine_id'] = machine_id
        
        logger.info(f"Preprocessing completed for machine {machine_id}")
        return df

    @staticmethod
    def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values using interpolation"""
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                df[col] = df[col].interpolate(method='linear', limit_direction='both')
                logger.info(f"Filled {missing_count} missing values in {col}")
        
        return df

    @staticmethod
    def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
        """Create lag and rolling features"""
        df = df.copy()
        
        # Lag features
        for lag in [1, 3, 7]:
            for col in ['temperature', 'vibration', 'pressure']:
                if col in df.columns:
                    df[f'{col}_lag_{lag}'] = df[col].shift(lag)
        
        # Rolling statistics
        for window in [7, 14]:
            for col in ['temperature', 'vibration', 'pressure']:
                if col in df.columns:
                    df[f'{col}_rolling_mean_{window}'] = df[col].rolling(window=window).mean()
                    df[f'{col}_rolling_std_{window}'] = df[col].rolling(window=window).std()
        
        # Drop NaN rows from feature engineering
        df = df.dropna()
        
        logger.info(f"Feature engineering completed. Shape: {df.shape}")
        return df

    @staticmethod
    def normalize_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
        """Normalize numeric features"""
        df = df.copy()
        normalization_params = {}
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            mean = df[col].mean()
            std = df[col].std()
            
            if std > 0:
                df[col] = (df[col] - mean) / std
                normalization_params[col] = {'mean': mean, 'std': std}
        
        logger.info(f"Data normalized. Params: {normalization_params}")
        return df, normalization_params