#!/bin/bash

# Set application and model details
APP_NAME="llm-app"
VENV_DIR="venv"
MAIN_SCRIPT="src/main.py"
OLLAMA_MODEL="deepseek-r1-14b"

sudo apt update && sudo apt install -y libpq-dev python3-dev build-essential

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

# Check if Ollama is installed, install if missing
if ! command -v ollama &>/dev/null; then
    echo "⬇️ Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to install Ollama."
        exit 1
    fi
else
    echo "✅ Ollama is already installed."
fi

# Start Ollama daemon if not running
if ! pgrep -x "ollama" > /dev/null; then
    echo "🔄 Starting Ollama daemon..."
    ollama serve & disown
    sleep 3  # Wait for Ollama to start
else
    echo "✅ Ollama is already running."
fi

# Pull the required model if not available
if ! ollama list | grep -q "$OLLAMA_MODEL"; then
    echo "⬇️ Downloading Ollama model: $OLLAMA_MODEL..."
    ollama pull "$OLLAMA_MODEL"
else
    echo "✅ Model '$OLLAMA_MODEL' is already available."
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
