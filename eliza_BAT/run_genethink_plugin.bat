@echo off
echo ===================================
echo Genethink AI Plugin Runner
echo ===================================
echo.

set /p API_KEY=Enter Gemini API Key: 

echo.
echo Running Genethink AI Plugin with:
echo - API Key: [PROVIDED]
echo.

cd eliza_plugins\genethink_ai_plugin

python main.py --api_keys "%API_KEY%"

cd ..\..
echo.
echo Plugin execution complete.
echo.
pause
