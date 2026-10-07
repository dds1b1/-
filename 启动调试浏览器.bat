@echo off
chcp 65001 >nul
title Launch Edge for Upwork probe (with debug port)
cd /d "%~dp0"

set EDGE=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
if not exist "%EDGE%" set EDGE=C:\Program Files\Microsoft\Edge\Application\msedge.exe
if not exist "%EDGE%" (
  echo [!] Edge not found. Please edit this file and set the EDGE path.
  pause
  exit /b 1
)

set PROFILE=%CD%\upwork_edge_profile

echo ================================================================
echo   Launch Edge with remote debugging port 9222
echo ================================================================
echo.
echo   Edge will open with a dedicated profile folder:
echo     %PROFILE%
echo.
echo   This window is a REAL Edge (no automation), so Cloudflare
echo   will treat it like a normal browser - that is the whole point.
echo.
echo   Please do this in the window that opens:
echo     1) Log in to Upwork (only needed the first time)
echo     2) Open the talent search page and wait until you can
echo        actually see freelancer cards
echo     3) KEEP THIS BROWSER OPEN
echo.
echo   Then run:   python upwork_probe_cdp.py "logo design"
echo   (or double-click the probe bat)
echo ================================================================
echo.

start "" "%EDGE%" --remote-debugging-port=9222 --user-data-dir="%PROFILE%" --no-first-run --no-default-browser-check "https://www.upwork.com/"

echo Edge launched. This console window can be closed.
timeout /t 5 >nul
