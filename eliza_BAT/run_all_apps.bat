@echo off
echo ===================================
echo Starting All NEXORA Applications
echo ===================================
echo.

echo Starting Flask API Server...
start cmd /k "cd /d C:\Users\aksha\Desktop\NEXORA FINAL PROJECT && python run.py"

echo Starting Genethink AI Streamlit Frontend...
start cmd /k "cd /d C:\Users\aksha\Desktop\NEXORA FINAL PROJECT\Eliza_code\PROJECT 2 && streamlit run frontend/app.py"

echo Starting MRI 3D Streamlit Frontend...
start cmd /k "cd /d C:\Users\aksha\Desktop\NEXORA FINAL PROJECT\Eliza_code\PROJECT && streamlit run 3d/app.py"

echo.
echo All applications started! Please check the opened command windows.
echo.
echo Press any key to close this window (applications will continue running)...
pause > nul
