#!/usr/bin/env python3
"""
Bot 24/7 - Executa o RoteiroBot continuamente com reinicialização automática
"""

import subprocess
import time
import sys
import os
import signal
from datetime import datetime
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_24_7.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BotRunner:
    def __init__(self):
        self.process = None
        self.running = True
        self.restart_count = 0
        self.max_restarts_per_hour = 10
        self.last_restart_time = time.time()
        
    def log_message(self, message):
        """Registra mensagem com timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
        logger.info(message)
    
    def start_bot(self):
        """Inicia o bot principal"""
        try:
            self.log_message("🚛 Iniciando RoteiroBot...")
            
            # Muda para o diretório do script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            os.chdir(script_dir)
            
            # Executa o bot
            self.process = subprocess.Popen(
                [sys.executable, "main.py"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            
            self.log_message(f"✅ Bot iniciado com PID: {self.process.pid}")
            return True
            
        except Exception as e:
            self.log_message(f"❌ Erro ao iniciar bot: {e}")
            return False
    
    def stop_bot(self):
        """Para o bot"""
        if self.process:
            try:
                self.log_message("🛑 Parando bot...")
                self.process.terminate()
                self.process.wait(timeout=10)
                self.log_message("✅ Bot parado com sucesso")
            except subprocess.TimeoutExpired:
                self.log_message("⚠️ Forçando parada do bot...")
                self.process.kill()
                self.process.wait()
            except Exception as e:
                self.log_message(f"❌ Erro ao parar bot: {e}")
            finally:
                self.process = None
    
    def is_bot_running(self):
        """Verifica se o bot está rodando"""
        if self.process is None:
            return False
        
        return_code = self.process.poll()
        return return_code is None
    
    def should_restart(self):
        """Verifica se deve reiniciar o bot"""
        current_time = time.time()
        
        # Reset contador se passou 1 hora
        if current_time - self.last_restart_time > 3600:
            self.restart_count = 0
            self.last_restart_time = current_time
        
        return self.restart_count < self.max_restarts_per_hour
    
    def run(self):
        """Executa o bot continuamente"""
        self.log_message("🤖 Bot Runner 24/7 iniciado")
        self.log_message("📝 Pressione Ctrl+C para parar completamente")
        
        try:
            while self.running:
                if not self.is_bot_running():
                    if self.should_restart():
                        self.restart_count += 1
                        self.log_message(f"🔄 Reiniciando bot... (tentativa {self.restart_count}/{self.max_restarts_per_hour})")
                        
                        if self.start_bot():
                            time.sleep(5)  # Aguarda estabilização
                        else:
                            self.log_message("❌ Falha ao iniciar bot, aguardando 30 segundos...")
                            time.sleep(30)
                    else:
                        self.log_message(f"❌ Máximo de reinicializações atingido ({self.max_restarts_per_hour})")
                        self.log_message("🛑 Encerrando Bot Runner")
                        break
                else:
                    # Bot está rodando, aguarda um pouco
                    time.sleep(10)
                    
        except KeyboardInterrupt:
            self.log_message("🛑 Bot Runner interrompido pelo usuário")
        except Exception as e:
            self.log_message(f"❌ Erro no Bot Runner: {e}")
        finally:
            self.stop_bot()
            self.log_message("👋 Bot Runner encerrado")

def signal_handler(signum, frame):
    """Handler para sinais do sistema"""
    logger.info("🛑 Sinal de parada recebido")
    sys.exit(0)

def main():
    """Função principal"""
    # Configura handlers de sinal
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Cria e executa o runner
    runner = BotRunner()
    runner.run()

if __name__ == "__main__":
    main()
