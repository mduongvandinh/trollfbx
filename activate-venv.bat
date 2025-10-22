@echo off
echo ========================================
echo  Activating Virtual Environment
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

echo Current directory: %cd%
echo.

cd backend

if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup-venv.bat first
    echo.
    pause
    exit /b 1
)

echo Virtual environment activated!
echo.
echo You can now run:
echo   python main.py         - Start backend server
echo   pip install package    - Install new packages
echo   pip list              - List installed packages
echo   deactivate            - Exit virtual environment
echo.

call venv\Scripts\activate.bat
cmd /k
