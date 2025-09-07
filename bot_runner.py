#!/usr/bin/env python3
"""
Bot Runner - Executa o RoteiroBot com reinicialização automática
"""

import subprocess
import time
import sys
import os
from datetime import datetime

def log_message(message):
    """Registra mensagem com timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def run_bot():
    """Executa o bot principal"""
    try:
        log_message("🚛 Iniciando RoteiroBot...")
        
        # Muda para o diretório do script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Executa o bot
        process = subprocess.Popen([sys.executable, "main.py"], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.STDOUT,
                                 universal_newlines=True,
                                 bufsize=1)
        
        # Monitora a saída
        for line in iter(process.stdout.readline, ''):
            if line:
                print(line.rstrip())
        
        process.wait()
        return process.returncode
        
    except KeyboardInterrupt:
        log_message("🛑 Bot interrompido pelo usuário")
        return 0
    except Exception as e:
        log_message(f"❌ Erro ao executar bot: {e}")
        return 1

def main():
    """Função principal com loop de reinicialização"""
    log_message("🤖 Bot Runner iniciado")
    log_message("📝 Pressione Ctrl+C para parar completamente")
    
    restart_count = 0
    max_restarts = 10  # Máximo de reinicializações por hora
    
    while True:
        try:
            return_code = run_bot()
            
            if return_code == 0:
                log_message("✅ Bot encerrado normalmente")
                break
            else:
                restart_count += 1
                log_message(f"⚠️ Bot encerrado com erro (código: {return_code})")
                
                if restart_count >= max_restarts:
                    log_message(f"❌ Máximo de reinicializações atingido ({max_restarts})")
                    log_message("🛑 Encerrando Bot Runner")
                    break
                
                log_message(f"🔄 Reiniciando em 5 segundos... (tentativa {restart_count}/{max_restarts})")
                time.sleep(5)
                
        except KeyboardInterrupt:
            log_message("🛑 Bot Runner interrompido pelo usuário")
            break
        except Exception as e:
            log_message(f"❌ Erro no Bot Runner: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
