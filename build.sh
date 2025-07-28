# Optional: install your dependencies
#!/usr/bin/env bash
# build.sh - Render will run this at build time

# Ensure directories
mkdir -p models

# Download the model
echo "Downloading model..."
curl -L -o models/best_model.pkl https://github.com/pauline12ish34/summative_linear_regression/releases/download/v1.0.0/best_model.pkl

echo "Model download complete."
pip install -r requirements.txt
