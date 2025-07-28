from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import requests

app = FastAPI()

# CORS Middleware - allow all for demo, adjust in prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_URL = "https://github.com/pauline12ish34/summative_linear_regression/releases/download/v1.0.0/best_model.pkl"
MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR / "best_model.pkl"

model = None  # Global model variable


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


def download_model():
    """Download the model file from GitHub release if not exists."""
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    if not MODEL_PATH.exists():
        print(f"Model not found locally. Downloading from {MODEL_URL} ...")
        response = requests.get(MODEL_URL)
        if response.status_code == 200:
            with open(MODEL_PATH, "wb") as f:
                f.write(response.content)
            print("Model downloaded successfully.")
        else:
            raise RuntimeError(f"Failed to download model, status code {response.status_code}")


def get_model():
    """Lazy load the model, download if missing."""
    global model
    if model is None:
        try:
            download_model()
            print("Loading model from disk...")
            loaded_model = joblib.load(MODEL_PATH)
            print("Model loaded successfully.")
            return loaded_model
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {str(e)}")
    return model


@app.post("/predict")
def predict_flood(data: FloodPredictionInput):
    global model
    if model is None:
        model = get_model()
    try:
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