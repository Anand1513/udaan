@echo off
echo ===================================================
echo   Starting Udaan Society Development Environment
echo ===================================================
echo.

echo [1/2] Starting Django Website (Port 8000)...
start "Django Website Server" cmd /k ".\venv\Scripts\activate && python manage.py runserver"

echo [2/2] Starting AI Chatbot Backend (Port 8001)...
start "AI Chatbot Server" cmd /k "cd ai_chatbot && .\venv\Scripts\activate && uvicorn app.main:app --reload --port 8001"

echo.
echo Both servers are launching in new windows!
echo.
echo Website URL: http://127.0.0.1:8000
echo Chatbot API: http://127.0.0.1:8001/docs
echo.
echo (Keep the new black terminal windows open while you work. Close them to stop the servers.)
echo ===================================================
pause
