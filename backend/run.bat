@echo off
REM Run the FastAPI backend server on Windows

cd /d "%~dp0" || exit /b

REM Create .env file if it doesn't exist
if not exist .env (
    copy .env.example .env
    echo Created .env file from .env.example - please configure it
)

REM Run the server
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload

pause
