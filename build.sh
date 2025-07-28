#!/usr/bin/env bash
set -o errexit

# Install Git LFS and fetch large files (like .pkl)
git lfs install
git lfs pull

# Optional: install your dependencies
pip install -r requirements.txt
