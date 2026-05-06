@echo off
set /p name=Enter your name:
if /I "%name%"=="admin" (
    echo Hello admin!
) else (
    echo Hello %name%, you are not an admin.
)
pause