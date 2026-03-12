from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
import pandas as pd
from app.model.anomaly_detector import AnomalyDetector
from app.model.forecaster import Forecaster
import json

router = APIRouter()
detector = AnomalyDetector(contamination="auto")
forecaster = Forecaster(steps_to_predict=3)

# Global store for simplicity in this demo to allow GET /anomalies
# In a real system, use a database.
LATEST_RESULTS = {
    "data": [],
    "stats": {
        "total_readings": 0,
        "anomaly_count": 0,
        "avg_energy": 0.0
    }
}

class AnomalyStats(BaseModel):
    total_readings: int
    anomaly_count: int
    avg_energy: float

class AnomalyResponse(BaseModel):
    data: List[Dict[str, Any]]
    stats: AnomalyStats

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    allowed_extensions = ('.csv', '.xlsx', '.xls')
    if not file.filename.lower().endswith(allowed_extensions):
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload CSV or Excel files.")
    
    content = await file.read()
    try:
        from app.services.data_processing import process_file
        df = process_file(content, file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Needs at least a feature column, let's assume 'energy' or use the first numeric column
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if not numeric_cols:
        raise HTTPException(status_code=400, detail="No numeric columns found in the CSV for anomaly detection.")
    
    # Use 'energy' if available, else first numeric
    feature_col = 'energy' if 'energy' in df.columns else numeric_cols[0]
    
    # Add a timestamp column if not exists for front-end charting
    time_col = 'timestamp' if 'timestamp' in df.columns else None
    if time_col and not pd.api.types.is_datetime64_any_dtype(df[time_col]):
        try:
            df[time_col] = pd.to_datetime(df[time_col])
        except:
            pass
            
    # Process anomalies
    try:
        result_df = detector.fit_predict(df, [feature_col])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Anomaly detection failed: {str(e)}")
    
    # Prepare results
    records = result_df.to_dict(orient='records')
    
    # Format for frontend: ensure we have something to plot
    chart_data = []
    for i, r in enumerate(records):
        time_val = str(r[time_col]) if time_col else f"Point {i}"
        chart_data.append({
            "id": i,
            "time": time_val,
            "value": r[feature_col],
            "is_anomaly": bool(r['is_anomaly']),
            "anomaly_score": r['anomaly_score'],
            "is_forecast": False
        })
        
    # Attempt to forecast the next 3 points
    try:
        future_points = forecaster.predict_future(df, feature_col, time_col)
        if future_points and len(chart_data) > 0:
            # Anchor the forecast line to the last historical point
            chart_data[-1]["forecast_value"] = chart_data[-1]["value"]
            for fp in future_points:
                fp["forecast_value"] = fp.pop("value")
                chart_data.append(fp)
    except Exception as e:
        # Silently fail if forecasting is not possible
        pass
    
    # Stats
    total = len(result_df)
    anomalies = int(result_df['is_anomaly'].sum())
    avg_energy = float(result_df[feature_col].mean())
    
    LATEST_RESULTS["data"] = chart_data
    LATEST_RESULTS["stats"] = {
        "total_readings": total,
        "anomaly_count": anomalies,
        "avg_energy": avg_energy
    }
    
    return {"message": "File processed successfully", "stats": LATEST_RESULTS["stats"]}

@router.get("/anomalies", response_model=AnomalyResponse)
async def get_anomalies():
    return LATEST_RESULTS
