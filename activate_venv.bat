@echo off
REM Custom activation script for Kilocode to use conda environment
REM This script explicitly sets up the conda environment for Kilocode terminals

echo Activating conda environment: D:\AI-ML\venv-global

REM Set Python environment variables
set PYTHONHOME=D:\AI-ML\venv-global
set PYTHONPATH=D:\AI-ML\venv-global\Lib\site-packages
set PATH=D:\AI-ML\venv-global;D:\AI-ML\venv-global\Scripts;D:\AI-ML\venv-global\Library\bin;%PATH%

REM Verify activation
echo.
echo Python environment activated:
D:\AI-ML\venv-global\python.exe -c "import sys; print(f'Python: {sys.executable}'); print(f'Version: {sys.version.split()[0]}'); print(f'Environment: {sys.prefix}')"

echo.
echo Conda environment is now active for this terminal session.