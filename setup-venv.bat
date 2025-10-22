@echo off
echo ========================================
echo  Setup Virtual Environment - Backend
echo ========================================
echo.

REM Save current directory and change to script directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Current directory: %cd%
echo.

echo Step 1: Creating virtual environment...
cd backend

if not exist "%cd%" (
    echo ERROR: backend folder not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

echo Creating venv in: %cd%\venv
python -m venv venv

if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 3: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 4: Installing dependencies...
pip install -r ../requirements.txt

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Virtual environment created at: backend\venv
echo.
echo To activate venv in the future:
echo   cd backend
echo   venv\Scripts\activate.bat
echo.
echo Then run:
echo   python main.py
echo.
pause
