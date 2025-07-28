import os
import aiohttp
import joblib

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path


app = FastAPI()

# Configuration
MODEL_URL = "https://github.com/pauline12ish34/summative_linear_regression/releases/download/v1.0.0/best_model.pkl"
MODEL_PATH = Path("models/best_model.pkl")
CHUNK_SIZE = 8192  # Download chunk size in bytes

class ModelLoader:
    _instance = None
    model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def download_model(self):
        """Async download from GitHub Releases"""
        MODEL_PATH.parent.mkdir(exist_ok=True)
        
        if not MODEL_PATH.exists():
            print("Downloading model from GitHub Releases...")
            async with aiohttp.ClientSession() as session:
                async with session.get(MODEL_URL) as response:
                    if response.status == 200:
                        with open(MODEL_PATH, 'wb') as f:
                            while True:
                                chunk = await response.content.read(CHUNK_SIZE)
                                if not chunk:
                                    break
                                f.write(chunk)
                        print("Model downloaded successfully")
                    else:
                        raise HTTPException(
                            status_code=500,
                            detail=f"Failed to download model: HTTP {response.status}"
                        )

    async def load_model(self):
        """Load model into memory"""
        if not MODEL_PATH.exists():
            await self.download_model()
        
        try:
            self.model = joblib.load(MODEL_PATH)
            print("Model loaded successfully")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Model loading failed: {str(e)}"
            )

# Initialize model on startup
@app.on_event("startup")
async def startup_event():
    loader = ModelLoader()
    await loader.load_model()

@app.get("/model-info")
async def model_info():
    """Check model status"""
    return {
        "model_loaded": ModelLoader().model is not None,
        "model_path": str(MODEL_PATH),
        "model_size": f"{os.path.getsize(MODEL_PATH) / (1024 * 1024):.2f} MB" 
        if MODEL_PATH.exists() else None
    }

@app.post("/predict")
async def predict(features: dict):
    """Make predictions"""
    if ModelLoader().model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Add your preprocessing here
        processed_features = preprocess(features)
        prediction = ModelLoader().model.predict([processed_features])
        return {"prediction": prediction.tolist()[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def preprocess(input_data: dict) -> list:
    """Example preprocessing - customize for your model"""
    return [
        float(input_data.get("feature1", 0)),
        float(input_data.get("feature2", 0)),
        # Add other features
    ]

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)