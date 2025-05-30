@echo off
setlocal enabledelayedexpansion

echo === Folder Deletion Utility ===
echo Enter full folder paths to delete, one per line.
echo Type DONE when you are finished.
echo.

set i=0

:input_loop
set /p folderPath=Enter folder path [%i%]: 
if /i "%folderPath%"=="DONE" goto delete_folders
if exist "%folderPath%" (
    set /a i+=1
    set "folders[!i!]=%folderPath%"
) else (
    echo Folder not found: %folderPath%
)
goto input_loop

:delete_folders
if %i%==0 (
    echo No valid folder paths provided. Exiting.
    goto end
)

echo.
echo === Confirm Deletion ===
for /L %%j in (1,1,%i%) do (
    echo [%%j] !folders[%%j]!
)
echo.

set /p confirm=Are you sure you want to delete these folders? (Y/N): 
if /i not "%confirm%"=="Y" (
    echo Deletion cancelled.
    goto end
)

echo.
echo === Deleting Folders ===
for /L %%j in (1,1,%i%) do (
    echo Deleting !folders[%%j]! ...
    rd /s /q "!folders[%%j]!"
    if not exist "!folders[%%j]!" (
        echo Deleted: !folders[%%j]!
    ) else (
        echo Failed to delete: !folders[%%j]!
    )
)
echo Done.

:end
endlocal
pause
