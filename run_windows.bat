@echo off
cd /d "%~dp0"
gcc -std=c11 -Wall -Wextra -O2 c_core\main.c -o similarity_engine.exe
if errorlevel 1 (echo GCC compilation failed. Check GCC and PATH.&pause&exit /b 1)
python -m pip install -r requirements.txt
if errorlevel 1 (echo Could not install Python requirements. Check your internet connection.&pause&exit /b 1)
python server.py
pause
