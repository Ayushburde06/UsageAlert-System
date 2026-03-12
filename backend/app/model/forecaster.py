import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class Forecaster:
    def __init__(self, steps_to_predict=3):
        self.steps = steps_to_predict
        self.model = LinearRegression()

    def predict_future(self, df: pd.DataFrame, feature_column: str, time_col: str = None) -> list:
        if len(df) < 2:
            return []
            
        x_train = np.arange(len(df)).reshape(-1, 1)
        y_train = df[feature_column].values
        
        self.model.fit(x_train, y_train)
        
        x_future = np.arange(len(df), len(df) + self.steps).reshape(-1, 1)
        y_future = self.model.predict(x_future)
        
        future_data = []
        for i in range(self.steps):
            future_val = float(y_future[i])
            
            # Simple timestamp generation
            time_val = f"Forecast +{i+1}"
            if time_col and pd.api.types.is_datetime64_any_dtype(df[time_col]):
                try:
                    delta = (df[time_col].iloc[-1] - df[time_col].iloc[0]) / len(df)
                    # Create a clean string without pandas Timedelta complexities
                    time_val = str(df[time_col].iloc[-1] + delta * (i + 1))
                except:
                    pass
            
            future_data.append({
                "id": len(df) + i,
                "time": time_val,
                "value": future_val,  # Will pop this out in endpoints.py
                "is_anomaly": False,
                "anomaly_score": 0.0,
                "is_forecast": True
            })
            
        return future_data
