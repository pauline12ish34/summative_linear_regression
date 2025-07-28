from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Model with ALL 20 attributes (exactly matching your dataset)
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

# Load the model (ensure the path is correct)
MODEL_PATH = "../best_model.pkl"
if not os.path.exists(MODEL_PATH):
    raise RuntimeError("Model file not found. Train the model first!")

model = joblib.load(MODEL_PATH)

@app.post("/predict")
def predict_flood(data: FloodPredictionInput):
    try:
        # Convert input data to numpy array in the correct order
        input_data = np.array([[
            data.MonsoonIntensity,
            data.TopographyDrainage,
            data.RiverManagement,
            data.Deforestation,
            data.Urbanization,
            data.ClimateChange,
            data.DamsQuality,
            data.Siltation,
            data.AgriculturalPractices,
            data.Encroachments,
            data.IneffectiveDisasterPreparedness,
            data.DrainageSystems,
            data.CoastalVulnerability,
            data.Landslides,
            data.Watersheds,
            data.DeterioratingInfrastructure,
            data.PopulationScore,
            data.WetlandLoss,
            data.InadequatePlanning,
            data.PoliticalFactors
        ]])
        prediction = model.predict(input_data)
        return {"predicted_flood_probability": float(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))