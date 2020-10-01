@echo off
call :deleteSelf&exit /b
:deleteSelf
python "%~dp0\src\UNINSTALLmain.py"
start /b "" cmd /c del "%~f0"&exit /b