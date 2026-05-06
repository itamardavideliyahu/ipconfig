@echo off
REM Hide command echoing to keep output clean.

setlocal
REM Start local scope for variables (changes end when script exits).

set LOGFILE=network_check.log
REM Define log file name for saved results.

echo ===== Network Check Started: %date% %time% ===== >> %LOGFILE%
REM Append start timestamp to log file (>> means append, not overwrite).

for %%H in (8.8.8.8 1.1.1.1 google.com) do (
    REM Loop over each host/IP in the list. In .bat files we use %%H.

    ping -n 1 %%H >nul
    REM Send 1 ping packet. Redirect output to NUL to hide ping details.

    if errorlevel 1 (
        REM errorlevel 1 means ping failed (host unreachable / no reply).
        echo [FAIL] %%H - No response >> %LOGFILE%
        echo %%H is not reachable
    ) else (
        REM Otherwise ping succeeded.
        echo [OK] %%H - Reachable >> %LOGFILE%
        echo %%H is reachable
    )
)

echo ===== Check Finished: %date% %time% ===== >> %LOGFILE%
REM Append end timestamp to log file.

echo results saved in %LOGFILE%
REM Inform user where results are stored.

pause
REM Wait for key press so terminal window does not close immediately.