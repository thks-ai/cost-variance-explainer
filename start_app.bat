@echo off
call venv\Scripts\activate
start "" cmd /c "uvicorn app.main:app --reload"
timeout /t 5 >nul
start http://localhost:8000




