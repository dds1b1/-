@echo off
chcp 65001 >nul
title Clean and dedupe profiles.csv
cd /d "%~dp0"

set PY=python
python --version >nul 2>nul
if errorlevel 1 (
  echo [!] Python not found. Install Python 3.10+ first.
  echo     Make sure typing "python" in a terminal works.
  pause
  exit /b 1
)

echo ================================================================
echo   Clean and dedupe profiles.csv
echo ================================================================
echo.
echo   What this does:
echo     1) make a backup copy of profiles.csv first
echo     2) drop duplicated person_id
echo     3) turn newlines inside long text fields into spaces
echo.
echo   The script and the csv are BOTH in this folder.
echo   Just double-click this file; nothing else to configure.
echo ================================================================
echo.

REM The script file name is Chinese, so it is written as \uXXXX escapes
REM to keep this bat file pure ASCII (cmd.exe would garble raw Chinese).
python -c "import runpy;runpy.run_path('\u6e05\u6d17\u53bb\u91cd.py',run_name='__main__')"
if errorlevel 1 echo [!] The cleaning script exited with an error. See the message above.

echo.
echo ----------------------------------------------------------------
echo   Read the report above. Target:
echo     duplicate = 0   and   description-with-newline = 0
echo ----------------------------------------------------------------
echo.
pause
