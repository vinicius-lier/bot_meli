@echo off
title RoteiroBot - Background Service 24/7
echo.
echo ========================================
echo    RoteiroBot - Servico 24/7
echo ========================================
echo.
echo Iniciando bot em background...
echo.

cd /d "%~dp0"

REM Para qualquer processo anterior
taskkill /f /im python.exe /fi "WINDOWTITLE eq RoteiroBot*" 2>nul
taskkill /f /im python.exe /fi "COMMANDLINE eq *bot_24_7.py*" 2>nul

REM Executa o bot em background (nova janela)
start "RoteiroBot-24-7" /min python bot_simples_24_7.py

echo Bot iniciado em background 24/7!
echo.
echo O bot agora roda continuamente e se reinicia automaticamente
echo se houver algum problema.
echo.
echo Para parar o bot:
echo 1. Use o arquivo "stop_bot.bat"
echo 2. Ou abra o Gerenciador de Tarefas e finalize "python.exe"
echo.
echo Logs do bot: bot_24_7.log
echo.
pause
