@echo off
title LLM Transcriber
cls
echo =====================================================================
echo                         LLM TRANSCRIBER
echo =====================================================================
echo.

:: Create library directory if it does not exist
if not exist lib (mkdir lib)

set PYTHON_CMD=python
set NEED_PYTHON_INSTALL=0
set PYTHONDONTWRITEBYTECODE=1

:: 1. Check if an official clean native Python 3.14 standalone installation exists
if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python314\python.exe" (
    set PYTHON_CMD="%USERPROFILE%\AppData\Local\Programs\Python\Python314\python.exe"
    goto :CHECK_VENV
)

:: 2. Check if 'python' is available in the global system PATH
where python >nul 2>nul
if %errorlevel% neq 0 (
    goto :INSTALL_PYTHON
)

:: 3. Verify the global python is not MSYS2/MinGW and version is compatible (>= 3.10)
python -c "import sys; exit(1 if ('msys' in sys.executable.lower() or 'mingw' in sys.executable.lower() or sys.version_info < (3, 10)) else 0)" >nul 2>nul
if %errorlevel% neq 0 (
    goto :INSTALL_PYTHON
)

:: If all checks pass, global python is safe to use
set PYTHON_CMD=python
goto :CHECK_VENV


:INSTALL_PYTHON
:: Notify the user about missing or incompatible environment
powershell -Command "Write-Host '[WARNING] Incompatible or obsolete Python environment found (MSYS2 or version < 3.10)!' -ForegroundColor Yellow"
echo [INFO] Downloading official Python 3.14.6 installer...

:: Download official Python Windows installer binary via curl (ignoring revocation checks to bypass schannel limits)
curl --ssl-no-revoke -L -o lib\installer.exe https://www.python.org/ftp/python/3.14.6/python-3.14.6-amd64.exe

:: Check if the installer was successfully downloaded
if not exist lib\installer.exe (
    powershell -Command "Write-Host '[ERROR] Download failed. Please check your internet connection.' -ForegroundColor Red"
    pause
    exit
)

echo [INFO] Installing Python silently, please wait...
echo [INFO] Click YES if a Windows User Account Control (UAC) prompt appears.

:: Execute silent installation, adding Python to the user PATH environment
start /wait lib\installer.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
del lib\installer.exe

echo.

:: Confirm successful installation
powershell -Command "Write-Host '[OK] Python 3.14.6 installed successfully!' -ForegroundColor Green"

:: Refresh the executable path variable for the current active process
if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python314\python.exe" (
    set PYTHON_CMD="%USERPROFILE%\AppData\Local\Programs\Python\Python314\python.exe"
) else (
    powershell -Command "Write-Host '[ERROR] Installation completed but executable was not found. Please restart the script.' -ForegroundColor Red"
    pause
    exit
)

:CHECK_VENV
:: Handle clean native Windows virtual environment creation
if not exist lib\MarkItDown\.venv (
    echo [INFO] First run detected. Initiating diagnostic tools...
    echo.
    
    :: Run system configuration script using the selected native Python
    %PYTHON_CMD% lib\setup.py
   
    echo [INFO] Creating native isolated virtual environment inside 'lib\MarkItDown'...
    if not exist lib\MarkItDown mkdir lib\MarkItDown
    %PYTHON_CMD% -m venv lib\MarkItDown\.venv
    echo [INFO] Installing all project dependencies: Transcription + MarkItDown. Please wait...
    
    :: Upgrade PIP package manager inside the newly created clean environment
    lib\MarkItDown\.venv\Scripts\python.exe -m pip install --upgrade pip
    
    :: Install core multimedia packages first, then explicitly fetch the latest MarkItDown release
    lib\MarkItDown\.venv\Scripts\pip.exe install yt-dlp yt-dlp-ejs faster-whisper nvidia-cublas-cu12 nvidia-cudnn-cu12
    lib\MarkItDown\.venv\Scripts\pip.exe install "markitdown[all]>=0.1.6" --ignore-requires-python

    :: Notify the user that environment setup is complete
    powershell -Command "Write-Host '[OK] Unified dependencies successfully configured!' -ForegroundColor Green"
    echo.

    cls
)

:: Check and download portable FFmpeg binaries if not present
if not exist lib\FFmpeg\ffmpeg.exe (
    echo [INFO] FFmpeg not found. Downloading standalone binaries...
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'lib\ffmpeg.zip'"
    echo [INFO] Extracting multimedia components...
    powershell -Command "Expand-Archive -Path 'lib\ffmpeg.zip' -DestinationPath 'lib\temp_ffmpeg' -Force"
    
    :: Create lib\FFmpeg folder if not exists
    if not exist "lib\FFmpeg" mkdir "lib\FFmpeg"
    copy /Y "lib\temp_ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe" "lib\FFmpeg\" >nul
    copy /Y "lib\temp_ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffprobe.exe" "lib\FFmpeg\" >nul    
    del /Q "lib\ffmpeg.zip" >nul 2>nul
    rmdir /S /Q "lib\temp_ffmpeg" >nul 2>nul

    cls
)

:: ---------------------------------------------------------------------
:: AUTOMATIC BACKGROUND UPDATES (ADDED SECTION)
:: ---------------------------------------------------------------------
:: Safely check and update yt-dlp on every launch to prevent YouTube scraping errors.
:: Using --quiet ensures it doesn't flood the window if there are no updates.
echo [INFO] Checking for critical yt-dlp core updates...
lib\MarkItDown\.venv\Scripts\python.exe -m pip install --upgrade yt-dlp --quiet
echo [OK] Core components verified.
echo.

cls
echo =====================================================================
echo                         LLM TRANSCRIBER
echo =====================================================================
echo.

:: Execute main transcription core script directly via the venv native python
lib\MarkItDown\.venv\Scripts\python.exe lib\video_audio_transcriber.py

echo.
echo =====================================================================
echo [END] Process finished. You can close this window.
echo =====================================================================
pause