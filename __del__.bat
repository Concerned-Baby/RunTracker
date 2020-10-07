call :deleteSelf&exit /b
:deleteSelf
start /b "" cmd /c del "%~f0"&exit /b