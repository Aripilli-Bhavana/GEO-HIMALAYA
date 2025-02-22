#!/bin/bash

# Set application and model details
APP_NAME="llm-app"
MODEL_DIR="models"
MODEL_FILE="mistral-7b-instruct-v0.2.Q5_K_M.gguf"
MODEL_URL="https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/$MODEL_FILE"
VENV_DIR="venv"
MAIN_SCRIPT="src/main.py"

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "❌ Error: Python3 is not installed. Please install it first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &>/dev/null; then
    echo "❌ Error: pip is not installed. Please install it first."
    exit 1
fi

# Create models directory if not exists
if [ ! -d "$MODEL_DIR" ]; then
    echo "📁 Creating models directory..."
    mkdir -p "$MODEL_DIR"
fi

# Download the model if it does not exist
if [ ! -f "$MODEL_DIR/$MODEL_FILE" ]; then
    echo "⬇️ Downloading model: $MODEL_FILE..."
    wget -O "$MODEL_DIR/$MODEL_FILE" "$MODEL_URL"
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to download model."
        exit 1
    fi
else
    echo "✅ Model already exists. Skipping download."
fi

# Create and activate virtual environment if not exists
if [ ! -d "$VENV_DIR" ]; then
    echo "🐍 Creating a virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Ensure venv was created properly
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "❌ Error: Virtual environment creation failed. Please check your Python installation."
    exit 1
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Fix for PEP 668: Use --break-system-packages if necessary
PIP_INSTALL="pip install"
if pip --version | grep -q "externally-managed-environment"; then
    PIP_INSTALL="pip install --break-system-packages"
fi

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    $PIP_INSTALL --upgrade pip
    $PIP_INSTALL -r requirements.txt
else
    echo "⚠️ Warning: requirements.txt not found. Skipping dependency installation."
fi

# Start the Flask app using Python
if [ -f "$MAIN_SCRIPT" ]; then
    echo "🚀 Running application..."
    python3 "$MAIN_SCRIPT"
else
    echo "❌ Error: $MAIN_SCRIPT not found. Please ensure your main script is at $MAIN_SCRIPT."
    exit 1
fi

# Success message
echo "✅ $APP_NAME is running at http://localhost:5000"

# Keep the virtual environment active
exec "$SHELL"
