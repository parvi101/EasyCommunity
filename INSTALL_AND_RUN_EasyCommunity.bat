@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  set PY=py -3
) else (
  set PY=python
)
if not exist .venv (
  %PY% -m venv .venv
  if errorlevel 1 goto :error
)
call .venv\Scripts\activate.bat
python -m pip install -r requirements.lock.txt
if errorlevel 1 goto :error
echo.
echo Starting EasyCommunity at http://127.0.0.1:8781
python -m uvicorn app:app --host 127.0.0.1 --port 8781
goto :eof
:error
echo Installation or startup failed. Review the error above.
exit /b 1
