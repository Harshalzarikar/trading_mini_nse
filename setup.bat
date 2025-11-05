@echo off
echo ========================================
echo NSE Trading Platform - Setup Script
echo ========================================
echo.

echo [1/6] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [3/6] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo [4/6] Running database migrations...
cd nse_project
python manage.py makemigrations
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Failed to run migrations
    cd ..
    pause
    exit /b 1
)
echo Database migrations completed!
echo.

echo [5/6] Creating superuser...
echo Please enter superuser credentials:
python manage.py createsuperuser
echo.

echo [6/6] Setup complete!
echo.
echo ========================================
echo To start the server, run:
echo   cd nse_project
echo   daphne -b 0.0.0.0 -p 8000 nse_project.asgi:application
echo.
echo Or use the start.bat script
echo ========================================
echo.

cd ..
pause
