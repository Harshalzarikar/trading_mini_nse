@echo off
echo ========================================
echo NSE Trading Platform - Issue Fixer
echo ========================================
echo.

echo [1/5] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Virtual environment not found. Run setup.bat first.
    pause
    exit /b 1
)
echo.

echo [2/5] Installing/Updating dependencies...
pip install --upgrade channels daphne yfinance
echo.

echo [3/5] Clearing Python cache...
cd nse_project
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo Cache cleared!
echo.

echo [4/5] Running migrations...
python manage.py makemigrations
python manage.py migrate
echo.

echo [5/5] Collecting static files...
python manage.py collectstatic --noinput
echo.

echo ========================================
echo Fixes applied! Now start the server:
echo.
echo For WebSocket support (recommended):
echo   daphne -b 0.0.0.0 -p 8000 nse_project.asgi:application
echo.
echo Or use the start.bat script
echo ========================================
echo.

cd ..
pause
