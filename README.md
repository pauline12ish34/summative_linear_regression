# 🌊 Flood Prediction System for Rwanda

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Mission
Climate enthusiasts are finding new ways to halt floods and other natural hazards. These natural hazards are disrupting the lives of many people in Rwanda. With the rising temperatures and unprecedented rains, Rwanda, whose large population depends on agriculture, is no longer getting enough meals. 

My mission is to contribute to solving climate change issues through software engineering. My exposure to coding at ALU has inspired me to develop systems that address community challenges. This flood prediction system aims to provide early warnings to vulnerable communities.

## Source of Dataset
https://www.kaggle.com/datasets/naiyakhalid/flood-prediction-dataset

!<img width="694" height="456" alt="image" src="https://github.com/user-attachments/assets/278236e2-4203-406c-a2c0-6834afa6b527" />



![Flood Prediction Dashboard](screenshots/dashboard.png)  
*Example prediction interface*

## 🚀 Features
- Real-time flood risk prediction
- Historical flood data analysis
- API endpoint for integration with weather apps
- Machine learning model with 85% accuracy

## 📦 Installation

### Prerequisites
- Python 3.10+
- Git

### Setup
```bash
# Clone repository
git clone https://github.com/yourusername/flood-prediction.git
cd flood-prediction

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

```
🖥️ Running the Application
bash
# Start FastAPI server
```bash
cd backend
uvicorn app:app --reload
Access the API at:
🔗 http://localhost:8000
📚 Interactive docs: http://localhost:8000/docs
```

🖥️ Running the mobile Application
bash
# Start FastAPI server
```bash
cd mobo-flood-app
flutter pub get
flutter run
```

