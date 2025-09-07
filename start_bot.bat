@echo off
title RoteiroBot - Sistema de Controle de Rotas
echo.
echo ========================================
echo    RoteiroBot - Sistema de Controle
echo ========================================
echo.
echo Iniciando bot...
echo.

cd /d "%~dp0"
python main.py

echo.
echo Bot foi encerrado. Pressione qualquer tecla para sair...
pause >nul
