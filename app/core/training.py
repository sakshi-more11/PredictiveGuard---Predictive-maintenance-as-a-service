import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import logging
from typing import Tuple, Dict, Any
from app.core.preprocessing import DataPreprocessor

logger = logging.getLogger(__name__)

class ModelTrainer:
    """Handles model training and evaluation"""

    @staticmethod
    def train_prophet_model(
        df: pd.DataFrame,
        machine_id: int
    ) -> Tuple[Prophet, Dict[str, Any]]:
        """Train Prophet model for time series forecasting"""
        
        try:
            # Prepare data for Prophet
            prophet_df = df[['timestamp', 'temperature']].copy()
            prophet_df.columns = ['ds', 'y']
            
            # Train model
            model = Prophet(
                yearly_seasonality=False,
                weekly_seasonality=True,
                daily_seasonality=False,
                interval_width=0.95
            )
            model.fit(prophet_df)
            
            # Evaluate on historical data (backtesting)
            future = model.make_future_dataframe(periods=30)
            forecast = model.predict(future)
            
            # Calculate metrics
            y_true = prophet_df['y'].values
            y_pred = forecast['yhat'][:len(y_true)].values
            
            mae = mean_absolute_error(y_true, y_pred)
            rmse = np.sqrt(mean_squared_error(y_true, y_pred))
            
            metrics = {
                "mae": float(mae),
                "rmse": float(rmse),
                "model_type": "prophet",
                "samples": len(y_true)
            }
            
            logger.info(f"Prophet model trained for machine {machine_id}: MAE={mae:.2f}, RMSE={rmse:.2f}")
            return model, metrics
            
        except Exception as e:
            logger.error(f"Model training failed: {str(e)}")
            raise

    @staticmethod
    def train_simple_degradation_model(
        df: pd.DataFrame,
        machine_id: int
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Train a simple degradation model
        Uses linear regression on sensor trends
        """
        
        try:
            # Extract features
            X = np.arange(len(df)).reshape(-1, 1)
            y = df['vibration'].values
            
            # Simple linear fit (degradation slope)
            coeffs = np.polyfit(X.flatten(), y, 2)
            
            model_dict = {
                "type": "polynomial_degradation",
                "coefficients": coeffs.tolist(),
                "machine_id": machine_id
            }
            
            # Metrics
            y_pred = np.polyval(coeffs, X.flatten())
            rmse = np.sqrt(mean_squared_error(y, y_pred))
            mae = mean_absolute_error(y, y_pred)
            
            metrics = {
                "mae": float(mae),
                "rmse": float(rmse),
                "model_type": "polynomial_degradation",
                "samples": len(y),
                "degradation_rate": float(coeffs[0])  # Rate of change
            }
            
            logger.info(f"Degradation model trained: MAE={mae:.2f}, RMSE={rmse:.2f}")
            return model_dict, metrics
            
        except Exception as e:
            logger.error(f"Degradation model training failed: {str(e)}")
            raise