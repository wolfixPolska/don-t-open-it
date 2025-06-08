@echo off
REM Get path to this script
set CURRENT_DIR=%~dp0

REM Path to portable Python inside WinPython
set PYTHON_PATH=%CURRENT_DIR%WPy64-312100\python\python.exe

REM Run your script
cd %CURRENT_DIR%pad
"%PYTHON_PATH%" "%CURRENT_DIR%pad/main.pyw"
