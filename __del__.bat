call :deleteSelf&exit /b
:deleteSelf
DEL "testdelete.txt"
DEL ".git"
DEL "css"
DEL "HTML Pages"
DEL "res"
DEL "Runners"
DEL "src"
DEL ".gitignore"
DEL "README.md"
DEL "xApplication.bat"
DEL "xGenerate.bat"
DEL "xUninstall.bat"
start /b "" cmd /c del "%~f0"&exit /b
