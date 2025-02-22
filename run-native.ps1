# Set application and model details
$APP_NAME = "llm-app"
$MODEL_DIR = "models"
$MODEL_FILE = "mistral-7b-instruct-v0.2.Q5_K_M.gguf"
$MODEL_URL = "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/$MODEL_FILE"
$VENV_DIR = "venv"
$MAIN_SCRIPT = "src/main.py"

# Function to download model with retries
function Download-Model {
    param (
        [string]$url,
        [string]$output
    )
    
    $attempts = 3
    for ($i = 1; $i -le $attempts; $i++) {
        try {
            Write-Host "Attempt ${i}: Downloading model..."
            Invoke-WebRequest -Uri $url -OutFile $output -UseBasicParsing
            if (Test-Path $output) {
                Write-Host "Model downloaded successfully."
                return
            }
        } catch {
            Write-Host "Error: Download failed. Retrying (${i}/$attempts)..."
            Start-Sleep -Seconds 5
        }
    }
    Write-Host "Error: Model download failed after multiple attempts."
    exit 1
}

# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python is not installed. Please install it first."
    exit 1
}

# Check if pip is installed
if (-not (Get-Command pip -ErrorAction SilentlyContinue)) {
    Write-Host "Error: pip is not installed. Please install it first."
    exit 1
}

# Create models directory if not exists
if (-not (Test-Path $MODEL_DIR)) {
    Write-Host "Creating models directory..."
    New-Item -ItemType Directory -Path $MODEL_DIR | Out-Null
}

# Download the model if it does not exist
if (-not (Test-Path "$MODEL_DIR\$MODEL_FILE")) {
    Download-Model -url $MODEL_URL -output "$MODEL_DIR\$MODEL_FILE"
} else {
    Write-Host "Model already exists. Skipping download."
}

# Create and activate virtual environment if not exists
if (-not (Test-Path $VENV_DIR)) {
    Write-Host "Creating a virtual environment..."
    python -m venv $VENV_DIR
}

# Ensure venv was created properly
if (-not (Test-Path "$VENV_DIR\Scripts\Activate.ps1")) {
    Write-Host "Error: Virtual environment creation failed."
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
& "$VENV_DIR\Scripts\Activate"

# Upgrade pip and install dependencies
if (Test-Path "requirements.txt") {
    Write-Host "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
} else {
    Write-Host "Warning: requirements.txt not found. Skipping dependency installation."
}

# Start the Flask app using Python
if (Test-Path $MAIN_SCRIPT) {
    Write-Host "Running application..."
    python "$MAIN_SCRIPT"
} else {
    Write-Host "Error: $MAIN_SCRIPT not found."
    exit 1
}

# Success message
Write-Host "$APP_NAME is running at http://localhost:5000"
