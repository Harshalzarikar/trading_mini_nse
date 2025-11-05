@echo off
echo ========================================
echo NSE Trading Platform - Starting Server
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Starting ASGI server with WebSocket support...
echo Server will be available at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

cd nse_project
daphne -b 0.0.0.0 -p 8000 nse_project.asgi:application
