@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "PYTHON_EXE=%LocalAppData%\Programs\Python\Python312\python.exe"

if exist "%PYTHON_EXE%" (
  "%PYTHON_EXE%" "%SCRIPT_DIR%run_file_upload_guard.py" %*
  exit /b %ERRORLEVEL%
)

python "%SCRIPT_DIR%run_file_upload_guard.py" %*
exit /b %ERRORLEVEL%
