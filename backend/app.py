from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import os

app = FastAPI()

# Allow all CORS origins for testing/demo purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load pre-downloaded model (make sure it's tracked using Git LFS)
MODEL_PATH = "../best_model.pkl"

if not os.path.exists(MODEL_PATH):
    raise RuntimeError("Model not found! Make sure you uploaded it with Git LFS.")

# Load the model (joblib will handle compressed files too)
model = joblib.load(MODEL_PATH)

# Define the expected input
class FloodPredictionInput(BaseModel):
    MonsoonIntensity: float
    TopographyDrainage: float
    RiverManagement: float
    Deforestation: float
    Urbanization: float
    ClimateChange: float
    DamsQuality: float
    Siltation: float
    AgriculturalPractices: float
    Encroachments: float
    IneffectiveDisasterPreparedness: float
    DrainageSystems: float
    CoastalVulnerability: float
    Landslides: float
    Watersheds: float
    DeterioratingInfrastructure: float
    PopulationScore: float
    WetlandLoss: float
    InadequatePlanning: float
    PoliticalFactors: float

@app.post("/predict")
def predict_flood(data: FloodPredictionInput):
    try:
        input_data = np.array([[getattr(data, field) for field in data.__fields__]])
        prediction = model.predict(input_data)
        return {"predicted_flood_probability": float(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))