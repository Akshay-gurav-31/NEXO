@echo off
color 0A
title Nexora Eliza Plugins Menu

:menu
cls
echo ====================================================
echo             NEXORA ELIZA PLUGINS MENU
echo ====================================================
echo.
echo  [1] Run MRI 3D Plugin - Brain tumor analysis
echo  [2] Run Genethink AI Plugin - Scientific hypothesis
echo  [3] Run NexoGPT Plugin - Medical AI assistant
echo  [4] Run NewsNX Plugin - Medical news aggregator
echo  [5] Start Nexora API Server - All plugins as API
echo.
echo  [0] Exit
echo.
echo ====================================================
echo.

set /p choice=Enter your choice (0-5): 

if "%choice%"=="1" goto mri3d
if "%choice%"=="2" goto genethink
if "%choice%"=="3" goto nexogpt
if "%choice%"=="4" goto newsnx
if "%choice%"=="5" goto api
if "%choice%"=="0" goto exit

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto menu

:mri3d
call run_mri3d_plugin.bat
goto menu

:genethink
call run_genethink_plugin.bat
goto menu

:nexogpt
call run_nexogpt_plugin.bat
goto menu

:newsnx
call run_newsnx_plugin.bat
goto menu

:api
call start.bat
goto exit

:exit
echo Thank you for using Nexora Eliza Plugins!
timeout /t 3 >nul
exit
