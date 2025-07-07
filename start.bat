@echo off
REM Activate the virtual environment and run app.py, then open the browser

REM Change directory to the project folder if needed
cd /d %~dp0

REM Activate the virtual environment (adjust 'venv' if your folder is named differently)
call venv\Scripts\activate

REM Start the Flask app in the background
start cmd /k python app.py

REM Wait a few seconds for the server to start (adjust if needed)
timeout /t 3 >nul

REM Open the default browser to the app
start http://localhost:5000