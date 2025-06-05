@echo off
echo ======================================
echo NEXORA ELIZA PLUGINS API SERVER - SETUP
echo ======================================
echo.
echo Checking and installing required packages...
pip install -r requirements.txt
echo.
echo Starting Flask API server at http://localhost:5000
echo.
echo Press CTRL+C to stop the server
echo.
python flask_app.py
