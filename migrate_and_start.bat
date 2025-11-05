@echo off
echo ========================================
echo NSE Trading Platform - Setup & Start
echo ========================================
echo.

echo [1/4] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)
echo.

echo [2/4] Running migrations for new models...
cd nse_project
python manage.py makemigrations
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Migration failed
    cd ..
    pause
    exit /b 1
)
echo.

echo [3/4] Creating profiles for existing users...
python manage.py shell -c "from django.contrib.auth.models import User; from trading.models import UserProfile; [UserProfile.objects.get_or_create(user=user) for user in User.objects.all()]"
echo.

echo [4/4] Starting server with WebSocket support...
echo.
echo ========================================
echo Server starting at: http://localhost:8000
echo.
echo NEW FEATURES AVAILABLE:
echo  - User Wallet (₹100,000 starting balance)
echo  - Watchlist
echo  - Stock Details
echo  - Search Stocks
echo  - Profile Page
echo  - Enhanced Trading with wallet validation
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

daphne -b 0.0.0.0 -p 8000 nse_project.asgi:application
