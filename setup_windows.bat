@echo off
REM Video Hook Analyzer - Windows Setup Script
REM This script sets up the project environment on Windows

echo.
echo ========================================
echo Video Hook Analyzer - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Python found. Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Install FFmpeg (if not already installed):
echo    Download from: https://ffmpeg.org/download.html
echo    Add FFmpeg to your system PATH
echo.
echo 2. Install and run Ollama:
echo    Download from: https://ollama.ai
echo    Run: ollama serve
echo    In another terminal, pull a model: ollama pull llama3.1
echo.
echo 3. Run the application:
echo    streamlit run app.py
echo.
echo 4. Open your browser to: http://localhost:8501
echo.
pause
