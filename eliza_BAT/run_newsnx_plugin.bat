@echo off
echo ===================================
echo NewsNX Plugin Runner
echo ===================================
echo.

set /p API_KEY=Enter NewsAPI Key: 
set /p QUERY=Enter news query (press Enter to skip): 
set /p CATEGORY=Enter category filter (press Enter to skip): 
set /p SEARCH_TERM=Enter search term (press Enter to skip): 
set /p PAGE_SIZE=Enter page size (default 20, press Enter to use default): 
if "%PAGE_SIZE%"=="" set PAGE_SIZE=20

echo.
echo Running NewsNX Plugin with:
echo - API Key: [PROVIDED]
if not "%QUERY%"=="" echo - Query: %QUERY%
if not "%CATEGORY%"=="" echo - Category: %CATEGORY%
if not "%SEARCH_TERM%"=="" echo - Search Term: %SEARCH_TERM%
echo - Page Size: %PAGE_SIZE%
echo.

cd eliza_plugins\newsnx_plugin

python main.py --api_key "%API_KEY%" --page_size %PAGE_SIZE% ^
    %QUERY:~0,1% --query "%QUERY%" %CATEGORY:~0,1% --category_filter "%CATEGORY%" ^
    %SEARCH_TERM:~0,1% --search_term "%SEARCH_TERM%"

cd ..\..
echo.
echo Plugin execution complete.
echo.
pause
