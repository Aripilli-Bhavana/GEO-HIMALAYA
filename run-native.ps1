# Set application and model details
$APP_NAME = "llm-app"
$VENV_DIR = "venv"
$MAIN_SCRIPT = "src/main.py"
$OLLAMA_MODEL = "mistral"

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

# Check if Ollama is installed, install if missing
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "⬇️ Installing Ollama..."
    $installerPath = "$env:TEMP\ollama.msi"
    Invoke-WebRequest -Uri "https://ollama.com/download/Ollama.msi" -OutFile $installerPath
    Start-Process -FilePath "msiexec.exe" -ArgumentList "/i $installerPath /quiet /norestart" -Wait
    if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
        Write-Host "❌ Error: Failed to install Ollama."
        exit 1
    }
} else {
    Write-Host "✅ Ollama is already installed."
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
