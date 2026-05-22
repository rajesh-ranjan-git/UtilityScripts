@echo off
setlocal enabledelayedexpansion

echo Scanning projects in: %CD%
echo --------------------------------

for /D %%G in (*) do (
    if exist "%%G\.git" (
        echo Entering %%G
        pushd "%%G"

        echo Running git pull --all in %%G
        git pull --all

        echo Going back...
        popd
        echo --------------------------------
    ) else (
        echo Skipped: %%G (not a git repository)
        echo --------------------------------
    )
)

echo All projects updated successfully!
pause
