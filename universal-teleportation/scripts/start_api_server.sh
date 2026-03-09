#!/bin/bash

# Robust server startup script for WekezaOmniOS
# Ensures correct working directory and Python path.

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the universal-teleportation directory
cd "$SCRIPT_DIR/.." || exit

echo "✅ Changed working directory to $(pwd)"

# Free up port 8000
echo "🧹 Clearing port 8000..."
lsof -t -i:8000 | xargs -r kill -9

# Start the server
echo "🚀 Starting API server on http://0.0.0.0:8000"
python3 -m uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload
