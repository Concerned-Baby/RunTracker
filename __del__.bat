call :deleteSelf&exit /b
:deleteSelf
DEL "testdelete.txt"
start /b "" cmd /c del "%~f0"&exit /b
