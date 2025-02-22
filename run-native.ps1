# Windows PowerShell script equivalent to the Bash script

# Set application and model details
$APP_NAME = "llm-app"
$MODEL_DIR = "models"
$MODEL_FILE = "mistral-7b-instruct-v0.2.Q5_K_M.gguf"
$MODEL_URL = "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/$MODEL_FILE"
$VENV_DIR = "venv"
$MAIN_SCRIPT = "src/main.py"

# Function to check if a command exists
function Command-Exists {
    param ($command)
    $null -ne (Get-Command $command -ErrorAction SilentlyContinue)
}

# Check if Python is installed
if (-not (Command-Exists "python")) {
    Write-Host "❌ Error: Python is not installed. Please install it first." -ForegroundColor Red
    exit 1
}

# Check if pip is installed
if (-not (Command-Exists "pip")) {
    Write-Host "❌ Error: pip is not installed. Please install it first." -ForegroundColor Red
    exit 1
}

# Create models directory if it doesn't exist
if (-not (Test-Path $MODEL_DIR)) {
    Write-Host "📁 Creating models directory..."
    New-Item -ItemType Directory -Path $MODEL_DIR | Out-Null
}

# Download the model if it does not exist
if (-not (Test-Path "$MODEL_DIR\$MODEL_FILE")) {
    Write-Host "⬇️ Downloading model: $MODEL_FILE..."
    Invoke-WebRequest -Uri $MODEL_URL -OutFile "$MODEL_DIR\$MODEL_FILE"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error: Failed to download model." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ Model already exists. Skipping download."
}

# Create and activate virtual environment if not exists
if (-not (Test-Path $VENV_DIR)) {
    Write-Host "🐍 Creating a virtual environment..."
    python -m venv $VENV_DIR
}

# Ensure venv was created properly
if (-not (Test-Path "$VENV_DIR\Scripts\Activate.ps1")) {
    Write-Host "❌ Error: Virtual environment creation failed. Please check your Python installation." -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..."
& "$VENV_DIR\Scripts\Activate"

# Upgrade pip
Write-Host "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
if (Test-Path "requirements.txt") {
    Write-Host "📦 Installing dependencies..."
    pip install -r requirements.txt
} else {
    Write-Host "⚠️ Warning: requirements.txt not found. Skipping dependency installation."
}

# Start the Flask app using Python
if (Test-Path $MAIN_SCRIPT) {
    Write-Host "🚀 Running application..."
    python $MAIN_SCRIPT
} else {
    Write-Host "❌ Error: $MAIN_SCRIPT not found. Please ensure your main script is at $MAIN_SCRIPT." -ForegroundColor Red
    exit 1
}

# Success message
Write-Host "✅ $APP_NAME is running at http://localhost:5000"

# Keep the PowerShell window open
cmd /k
