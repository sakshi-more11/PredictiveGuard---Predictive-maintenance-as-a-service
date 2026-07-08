import pandas as pd
import numpy as np
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class PredictionEngine:
    """Handles model inference and predictions"""

    @staticmethod
    def predict_rul(
        model: Any,
        machine_data: pd.DataFrame,
        horizon_days: int = 30
    ) -> Dict[str, Any]:
        """
        Predict Remaining Useful Life (RUL)
        
        Returns:
            - rul_estimate: Estimated days until failure
            - failure_probability: Probability of failure within horizon
            - confidence_intervals: Lower and upper bounds
            - top_features: Most influential sensors
        """
        
        try:
            # Get latest data point
            latest_data = machine_data.tail(1)
            
            # Generate forecast
            forecast = model.predict(steps=horizon_days)
            
            # Calculate RUL based on degradation
            # Simplified: if failure threshold is crossed in forecast, RUL is that point
            degradation_threshold = 0.8  # Arbitrary threshold
            
            rul_estimate = None
            for i, value in enumerate(forecast):
                if value > degradation_threshold:
                    rul_estimate = i
                    break
            
            if rul_estimate is None:
                rul_estimate = horizon_days
            
            # Calculate failure probability
            failure_probability = min(rul_estimate / horizon_days, 1.0)
            
            # Confidence intervals
            forecast_std = np.std(forecast)
            lower_ci = forecast.mean() - 1.96 * forecast_std
            upper_ci = forecast.mean() + 1.96 * forecast_std
            
            # Top features (mock implementation)
            top_features = [
                {"feature": "vibration", "importance": 0.35},
                {"feature": "temperature", "importance": 0.30},
                {"feature": "pressure", "importance": 0.20},
                {"feature": "humidity", "importance": 0.15}
            ]
            
            result = {
                "rul_estimate": float(rul_estimate),
                "failure_probability": float(failure_probability),
                "lower_confidence_interval": float(lower_ci),
                "upper_confidence_interval": float(upper_ci),
                "confidence_level": 0.95,
                "top_features": top_features
            }
            
            logger.info(f"Prediction generated: RUL={rul_estimate} days")
            return result
            
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise

    @staticmethod
    def interpret_prediction(prediction: Dict[str, Any]) -> str:
        """Generate human-readable interpretation"""
        rul = prediction["rul_estimate"]
        fail_prob = prediction["failure_probability"]
        
        if rul < 7 and fail_prob > 0.8:
            return "CRITICAL: Schedule maintenance immediately"
        elif rul < 14 and fail_prob > 0.6:
            return "WARNING: Schedule maintenance within a week"
        elif rul < 30 and fail_prob > 0.4:
            return "CAUTION: Monitor closely and plan maintenance"
        else:
            return "OK: Equipment operating normally"