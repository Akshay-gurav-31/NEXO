@echo off
echo ===================================
echo NexoGPT Plugin Runner
echo ===================================
echo.

set /p API_KEY=Enter Groq API Key: 
set /p PROMPT=Enter your medical query: 
set /p MAX_TOKENS=Enter max tokens (default 200, press Enter to use default): 
if "%MAX_TOKENS%"=="" set MAX_TOKENS=200

set /p TEMPERATURE=Enter temperature (default 0.7, press Enter to use default): 
if "%TEMPERATURE%"=="" set TEMPERATURE=0.7

echo.
echo Running NexoGPT Plugin with:
echo - API Key: [PROVIDED]
echo - Prompt: %PROMPT%
echo - Max Tokens: %MAX_TOKENS%
echo - Temperature: %TEMPERATURE%
echo.

cd eliza_plugins\nexogpt_plugin

python main.py --prompt "%PROMPT%" --api_key "%API_KEY%" --max_tokens %MAX_TOKENS% --temperature %TEMPERATURE%

cd ..\..
echo.
echo Plugin execution complete.
echo.
pause
