
from pathlib import Path
from agents.coordinator import AgentCoordinator
from fastapi.middleware.cors import CORSMiddleware
from database.db import init_db, save_analysis, get_history

import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel, Field

# Find project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Load trained model
MODEL_PATH = BASE_DIR / "models" / "flood_model.pkl"
model = joblib.load(MODEL_PATH)

# Initialize API
app = FastAPI(
    title="NIRNAYA AI",
    description="AI-powered Disaster Decision Intelligence",
    version="1.0.0"
)
init_db()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Initialize multi-agent coordinator
coordinator = AgentCoordinator()


# Input validation
class FloodInput(BaseModel):
    rainfall_mm: float = Field(ge=0, le=500)
    water_level_cm: float = Field(ge=0, le=500)
    drainage_capacity: float = Field(ge=0, le=100)
    previous_flooding: int = Field(ge=0, le=1)
    elevation_m: float = Field(ge=0, le=500)


@app.get("/")
def home():
    return {
        "project": "NIRNAYA AI",
        "status": "Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": True
    }



@app.post("/predict")
def predict_flood(data: FloodInput):

    input_data = pd.DataFrame([{
        "rainfall_mm": data.rainfall_mm,
        "water_level_cm": data.water_level_cm,
        "drainage_capacity": data.drainage_capacity,
        "previous_flooding": data.previous_flooding,
        "elevation_m": data.elevation_m
    }])

    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    confidence = float(max(probabilities))

    return {
        "project": "NIRNAYA AI",
        "flood_risk": str(prediction),
        "confidence": round(confidence, 4),
        "data_type": "Synthetic prototype"
    }

@app.post("/analyze")
def analyze_flood(data: FloodInput):

    flood_data = {
        "rainfall_mm": data.rainfall_mm,
        "water_level_cm": data.water_level_cm,
        "drainage_capacity": data.drainage_capacity,
        "previous_flooding": data.previous_flooding,
        "elevation_m": data.elevation_m
    }

    result = coordinator.run_all(flood_data)

    result["input"] = flood_data
    save_analysis(result)

    return result


@app.get("/history")
def analysis_history():
    return get_history()
