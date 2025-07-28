from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import requests

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model setup
MODEL_URL = "https://github.com/pauline12ish34/summative_linear_regression/releases/download/v1.0.0/best_model.pkl"
MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR / "best_model.pkl"
model = None

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
    """Download the model from GitHub if not present."""
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    if not MODEL_PATH.exists():
        print(f"Model not found. Downloading from {MODEL_URL} ...")
        response = requests.get(MODEL_URL)
        if response.status_code == 200:
            with open(MODEL_PATH, "wb") as f:
                f.write(response.content)
            print("Model downloaded successfully.")
        else:
            raise RuntimeError(f"Failed to download model, status code: {response.status_code}")

def load_model():
    """Load the model from disk."""
    global model
    try:
        download_model()
        model = joblib.load(MODEL_PATH)
        print(" Model loaded successfully.")
    except Exception as e:
        print(f" Failed to load model: {str(e)}")
        raise RuntimeError("Could not load model.")

@app.on_event("startup")
def startup_event():
    """Runs once when the app starts."""
    load_model()

@app.post("/predict")
def predict_flood(data: FloodPredictionInput):
    try:
        input_data = np.array([[getattr(data, field) for field in data.__fields__]])
        prediction = model.predict(input_data)
        return {"predicted_flood_probability": float(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
