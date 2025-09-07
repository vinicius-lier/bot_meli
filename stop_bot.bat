@echo off
title Parar RoteiroBot
echo.
echo ========================================
echo    Parando RoteiroBot 24/7
echo ========================================
echo.

echo Procurando processos do RoteiroBot...

REM Para processos Python relacionados ao bot
taskkill /f /im python.exe /fi "WINDOWTITLE eq RoteiroBot*" 2>nul
taskkill /f /im python.exe /fi "COMMANDLINE eq *main.py*" 2>nul
taskkill /f /im python.exe /fi "COMMANDLINE eq *bot_runner.py*" 2>nul
taskkill /f /im python.exe /fi "COMMANDLINE eq *bot_24_7.py*" 2>nul

echo.
echo Bot parado!
echo.
echo Se o bot não parou, use o Gerenciador de Tarefas
echo para finalizar manualmente os processos python.exe
echo.
pause
