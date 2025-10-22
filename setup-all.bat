@echo off
echo ========================================
echo  Setup Football Meme Super App
echo  Backend + Frontend
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

echo Current directory: %cd%
echo.

echo Step 1/2: Setting up Backend (with venv)...
echo ========================================
echo.

call setup-venv.bat

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Backend setup failed!
    echo.
    pause
    exit /b 1
)

echo.
echo.
echo Step 2/2: Setting up Frontend...
echo ========================================
echo.

call setup-frontend.bat

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Frontend setup failed!
    echo.
    pause
    exit /b 1
)

echo.
echo.
echo ========================================
echo  ALL SETUP COMPLETE!
echo ========================================
echo.
echo Backend: ✓ Virtual environment created
echo Frontend: ✓ npm packages installed
echo.
echo Next steps:
echo   1. Copy .env.example to .env
echo   2. Fill in your API keys in .env
echo   3. Run: start-backend-venv.bat
echo   4. Run: start-frontend.bat
echo.
pause
