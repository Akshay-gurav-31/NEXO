@echo off
echo ===================================
echo MRI 3D Plugin Runner
echo ===================================
echo.

set /p FILE_PATH=Enter path to MRI file (e.g., path/to/brain_tumor.nii.gz): 
set /p THRESHOLD=Enter threshold value (default 0.5, press Enter to use default): 
if "%THRESHOLD%"=="" set THRESHOLD=0.5

set /p MIN_SIZE=Enter minimum size (default 100, press Enter to use default): 
if "%MIN_SIZE%"=="" set MIN_SIZE=100

set /p API_KEY=Enter Gemini API Key (optional, press Enter to skip): 

echo.
echo Running MRI 3D Plugin with:
echo - File: %FILE_PATH%
echo - Threshold: %THRESHOLD%
echo - Min Size: %MIN_SIZE%
if not "%API_KEY%"=="" echo - API Key: [PROVIDED]
echo.

cd eliza_plugins\mri_3d_plugin

if "%API_KEY%"=="" (
    python main.py --file_path "%FILE_PATH%" --threshold %THRESHOLD% --min_size %MIN_SIZE%
) else (
    python main.py --file_path "%FILE_PATH%" --threshold %THRESHOLD% --min_size %MIN_SIZE% --gemini_api_key "%API_KEY%"
)

cd ..\..
echo.
echo Plugin execution complete.
echo.
pause
