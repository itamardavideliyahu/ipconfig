@echo off
REM ============================================================
REM  Daily Windows Server maintenance check (Batch - training)
REM  Read-only: system info, disks, services, network
REM  Run: double-click or "Daily-Maintenance.bat" from CMD
REM ============================================================

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "LOGDIR=%SCRIPT_DIR%logs"
if not exist "%LOGDIR%" mkdir "%LOGDIR%"

for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value 2^>nul') do set "DT=%%I"
if not defined DT set "DT=00000000000000"
set "LOGFILE=%LOGDIR%\maintenance_%DT:~0,8%_%DT:~8,6%.log"

call :Log "========================================"
call :Log "  Daily Maintenance Report (Batch)"
call :Log "========================================"
call :Log ""

call :Log "--- System ---"
call :Log "Computer:"
hostname
call :Log "User: %USERNAME%"
call :Log "Date/Time: %date% %time%"
call :Log ""

call :Log "OS (systeminfo):"
for /f "tokens=1* delims=:" %%a in ('systeminfo ^| findstr /B /C:"OS Name" /C:"OS Version" /C:"System Boot Time"') do call :Log "  %%a:%%b"
call :Log ""

call :Log "--- Disk space ---"
wmic logicaldisk where "DriveType=3" get DeviceID,FreeSpace,Size
call :Log "(FreeSpace and Size are in bytes - divide by 1073741824 for GB)"
call :Log ""

call :Log "--- Services ---"
set "SVCLIST=EventLog LanmanServer LanmanWorkstation W32Time Dnscache Spooler"
for %%s in (%SVCLIST%) do (
    sc query "%%s" >nul 2>&1
    if !errorlevel! equ 0 (
        for /f "tokens=4" %%t in ('sc query "%%s" ^| findstr /I "STATE"') do call :Log "%%s : %%t"
    ) else (
        call :Log "%%s : not found"
    )
)
call :Log ""

call :Log "--- Network ---"
call :Log "ipconfig (IPv4 / Gateway):"
ipconfig | findstr /I "IPv4 Gateway"
call :Log ""
call :Log "Ping 8.8.8.8:"
ping -n 2 8.8.8.8
call :Log ""

call :Log "--- Processes (count) ---"
for /f %%c in ('tasklist 2^>nul ^| find /c /v ""') do call :Log "Running processes: %%c"
call :Log ""

call :Log "========================================"
call :Log "Done. Log file:"
call :Log "%LOGFILE%"
call :Log "========================================"
echo.
echo Log saved to: %LOGFILE%
pause
goto :eof

:Log
echo %~1
echo %~1>> "%LOGFILE%"
goto :eof
