@echo off

title J.A.R.V.I.S. Launcher

echo.
echo ==========================================
echo          J.A.R.V.I.S. STARTING
echo ==========================================
echo.

cd /d D:\Projects\jarvis\backend

call venv\Scripts\activate.bat

echo Starting FastAPI backend...
start "JARVIS Backend" cmd /k "cd /d D:\Projects\jarvis\backend && call venv\Scripts\activate.bat && uvicorn app.main:app --reload"

timeout /t 3 /nobreak >nul

echo.
echo Starting React frontend...
start "JARVIS Frontend" cmd /k "cd /d D:\Projects\jarvis\frontend && npm run dev"

timeout /t 5 /nobreak >nul

echo.
echo Starting JARVIS Voice Assistant...
start "JARVIS Voice" cmd /k "cd /d D:\Projects\jarvis\backend && call venv\Scripts\activate.bat && python start_jarvis_voice.py"

echo.
echo ==========================================
echo       J.A.R.V.I.S. IS READY
echo ==========================================
echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:5173
echo.
echo This is MANUAL launch only.
echo JARVIS does NOT auto-start with Windows.
echo.
pause