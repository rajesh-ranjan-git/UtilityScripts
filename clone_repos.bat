@echo off
setlocal enabledelayedexpansion

:: File containing GitHub repo URLs
set "urlFile=repos.txt"

:: Check if file exists
if not exist "%urlFile%" (
    echo File "%urlFile%" not found!
    exit /b
)

:: Read and clone each repo
for /f "usebackq delims=" %%A in ("%urlFile%") do (
    set "repoUrl=%%A"
    if not "!repoUrl!"=="" (
        echo Cloning !repoUrl! ...
        git clone !repoUrl!
        echo.
    )
)

echo Done!
pause
