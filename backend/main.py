from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import json
import os

app = FastAPI(title="Car Price Prediction API")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model and metrics on startup
MODEL_PATH = "../models/best_model.pkl"
METRICS_PATH = "../reports/metrics.json"

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Warning: Could not load model: {e}")

class CarInput(BaseModel):
    MPG_city: float
    MPG_highway: float
    EngineSize: float
    Horsepower: float
    RPM: float
    Rev_per_mile: float
    Fuel_tank_capacity: float
    Passengers: int
    Length: float
    Wheelbase: float
    Width: float
    Turn_circle: float
    Rear_seat_room: float
    Luggage_room: float
    Weight: float
    Type: str
    AirBags: str
    DriveTrain: str
    Cylinders: str
    Man_trans_avail: str
    Origin: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Car Price Prediction API"}

@app.get("/health")
def health_check():
    if model is not None:
        return {"status": "healthy", "model_loaded": True}
    return {"status": "degraded", "model_loaded": False}

@app.post("/predict")
def predict_price(car: CarInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded")
    
    # Map Pydantic fields to the exact column names the model expects
    input_data = {
        'MPG.city': [car.MPG_city],
        'MPG.highway': [car.MPG_highway],
        'EngineSize': [car.EngineSize],
        'Horsepower': [car.Horsepower],
        'RPM': [car.RPM],
        'Rev.per.mile': [car.Rev_per_mile],
        'Fuel.tank.capacity': [car.Fuel_tank_capacity],
        'Passengers': [car.Passengers],
        'Length': [car.Length],
        'Wheelbase': [car.Wheelbase],
        'Width': [car.Width],
        'Turn.circle': [car.Turn_circle],
        'Rear.seat.room': [car.Rear_seat_room],
        'Luggage.room': [car.Luggage_room],
        'Weight': [car.Weight],
        'Type': [car.Type],
        'AirBags': [car.AirBags],
        'DriveTrain': [car.DriveTrain],
        'Cylinders': [car.Cylinders],
        'Man.trans.avail': [car.Man_trans_avail],
        'Origin': [car.Origin]
    }
    
    df = pd.DataFrame(input_data)
    
    try:
        prediction = model.predict(df)[0]
        # Our model predicts price in $1000s based on this dataset
        return {
            "predicted_price": round(prediction * 1000, 2),
            "currency": "USD"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/model-info")
def get_model_info():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, 'r') as f:
            data = json.load(f)
            return {"model_used": data.get("best_model", "Unknown")}
    return {"model_used": "Unknown"}

@app.get("/metrics")
def get_metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, 'r') as f:
            data = json.load(f)
            best_model_name = data.get("best_model")
            if best_model_name:
                return data["metrics"][best_model_name]
    return {"error": "Metrics not found"}
