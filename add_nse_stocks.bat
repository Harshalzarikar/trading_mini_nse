@echo off
echo ========================================
echo Adding NSE Stocks to Database
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Virtual environment not found
    pause
    exit /b 1
)
echo.

echo This will add/update 50 popular NSE stocks
echo Fetching live prices from yfinance...
echo This may take 2-3 minutes...
echo.

cd nse_project
python manage.py add_nse_stocks

echo.
echo ========================================
echo Done! Check the output above.
echo ========================================
echo.

cd ..
pause
