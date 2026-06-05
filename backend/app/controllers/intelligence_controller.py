from fastapi import status, HTTPException
from sqlmodel import Session
from app.controllers.fire_controller import _verify_active_user
from app.schemas.intelligence_schema import FireDataResponse, FirePredictionRequest
from app.api.nasa_api import base_url, nasa_api
import httpx
import joblib
from joblib import Memory
import pandas as pd


cachedir = './wildfire_model_cache'
memory = Memory(cachedir, verbose=0)
try:
    model = joblib.load('best_xgb.pkl')
except Exception as e:
    print(f"Production Warning: Model file not found: {e}")
    model = None
def assign_risk_label(code: int) -> str:
    mapping = {0: "Low", 1: "Moderate", 2: "High", 3: "Extreme"}
    return mapping.get(code, "Unknown")

@memory.cache
def run_cached_inference(features_json: str):
    if model is None:
        return [], []
    features_df = pd.read_json(features_json)
    predictions = model.predict(features_df)
    probabilities = model.predict_proba(features_df)
    return predictions.tolist(), probabilities.tolist()

async def query_intelligence_controller(user_id: int, prediction_request: FirePredictionRequest, db: Session):
  _verify_active_user(user_id, db)
  west_lon = prediction_request.west_longitude
  south_lat = prediction_request.south_latitude
  east_lon = prediction_request.east_longitude
  north_lat = prediction_request.north_latitude
  source = "VIIRS_NOAA20_NRT"
  day_range = 1
    
  prediction_url = f"https://firms.modaps.eosdis.nasa.gov/api/area/YOUR_API_KEY/{source}/{west_lon},{south_lat},{east_lon},{north_lat}/{day_range}"
  try:
      async with httpx.AsyncClient() as client:
            response = await client.get(prediction_url)
            response.raise_for_status() 
  except httpx.RequestError:
        raise HTTPException(status_code=503, detail="NASA FIRMS service unreachable.")

  raw_hotspots = response.json()
  if not raw_hotspots:
        return {"status": "success", "hotspots_found": 0, "data": []}
  df = pd.DataFrame(raw_hotspots)
    
  df['is_daytime'] = df['daynight'].map({'D': 1, 'N': 0}).fillna(0).astype(int) if 'daynight' in df.columns else 1
  df['confidence_num'] = df['confidence'].map({'low': 0, 'nominal': 1, 'high': 2}).fillna(0) if df['confidence'].dtype == 'O' else df['confidence']
    
  df['scan'] = pd.to_numeric(df['scan']).fillna(0.4)
  df['track'] = pd.to_numeric(df['track']).fillna(0.4)
  df['bright_ti4'] = pd.to_numeric(df['bright_ti4']).fillna(320.0)
  df['bright_ti5'] = pd.to_numeric(df['bright_ti5']).fillna(295.0)
  df['frp'] = pd.to_numeric(df['frp']).fillna(5.0)

  df['pixel_area'] = df['scan'] * df['track']
  df['thermal_diff'] = df['bright_ti4'] / df['bright_ti5']
  df['thermal_ratio'] = df['bright_ti4'] / df['bright_ti5']
  feature_order = [
        'track', 'scan', 'bright_ti5', 'bright_ti4', 'latitude', 'longitude',
        'is_daytime', 'confidence_num', 'pixel_area', 'thermal_diff', 'thermal_ratio'
    ]
  features_df = df[feature_order]
  features_json = features_df.to_json()
    
  predictions, probabilities = run_cached_inference(features_json)
    
  analyzed_results = []
  for index, hotspot in enumerate(raw_hotspots):
        pred_code = predictions[index]
        probs = probabilities[index]
        
        analyzed_results.append({
            "latitude": float(hotspot.get("latitude")),
            "longitude": float(hotspot.get("longitude")),
            "predicted_risk_level": assign_risk_label(pred_code),
            "confidence_probabilities": {
                "Low": float(probs[0]),
                "Moderate": float(probs[1]),
                "High": float(probs[2]),
                "Extreme": float(probs[3])
            }
        })
        
  return {
        "status": "success",
        "hotspots_found": len(analyzed_results),
        "data": analyzed_results
    }