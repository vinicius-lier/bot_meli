#!/usr/bin/env python3
"""
Monitor de Saúde do RoteiroBot
Monitora continuamente o status do bot e resolve conflitos automaticamente
"""

import asyncio
import logging
import time
from datetime import datetime
from telegram import Bot
from telegram.error import Conflict, NetworkError
from config import TELEGRAM_BOT_TOKEN

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class BotMonitor:
    """Monitor de saúde do bot"""
    
    def __init__(self):
        self.bot = None
        self.running = False
        self.check_interval = 30  # Verifica a cada 30 segundos
        self.last_check = None
        self.consecutive_failures = 0
        self.max_failures = 3
        
    async def initialize(self):
        """Inicializa o monitor"""
        if not TELEGRAM_BOT_TOKEN:
            print("❌ ERRO: Token do Telegram não encontrado!")
            return False
        
        try:
            self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
            bot_info = await self.bot.get_me()
            print(f"✅ Monitor inicializado para: @{bot_info.username}")
            return True
        except Exception as e:
            print(f"❌ Erro ao inicializar monitor: {e}")
            return False
    
    async def check_bot_health(self):
        """Verifica a saúde do bot"""
        try:
            # Verifica se o bot responde
            bot_info = await self.bot.get_me()
            
            # Verifica webhook
            webhook_info = await self.bot.get_webhook_info()
            
            # Verifica updates pendentes
            updates = await self.bot.get_updates(limit=1, timeout=1)
            
            status = {
                'bot_active': True,
                'bot_username': bot_info.username,
                'webhook_active': bool(webhook_info.url),
                'webhook_url': webhook_info.url,
                'pending_updates': len(updates),
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
            
            self.consecutive_failures = 0
            return status
            
        except Conflict as e:
            logger.warning(f"Conflito detectado durante monitoramento: {e}")
            return {
                'bot_active': False,
                'conflict_detected': True,
                'error': str(e),
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
            
        except (NetworkError, Exception) as e:
            logger.warning(f"Erro durante verificação: {e}")
            self.consecutive_failures += 1
            return {
                'bot_active': False,
                'error': str(e),
                'consecutive_failures': self.consecutive_failures,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
    
    async def resolve_conflict(self):
        """Resolve conflitos automaticamente"""
        try:
            print("🔧 Resolvendo conflito automaticamente...")
            
            # Remove webhook
            await self.bot.delete_webhook(drop_pending_updates=True)
            print("✅ Webhook removido")
            
            # Aguarda
            await asyncio.sleep(3)
            
            # Limpa updates pendentes
            updates = await self.bot.get_updates(limit=100, timeout=1)
            if updates:
                print(f"📨 Limpando {len(updates)} updates pendentes...")
                for update in updates:
                    try:
                        await self.bot.get_updates(
                            offset=update.update_id + 1, 
                            limit=1, 
                            timeout=1
                        )
                    except:
                        pass
            
            await asyncio.sleep(2)
            print("✅ Conflito resolvido automaticamente")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao resolver conflito: {e}")
            return False
    
    def print_status(self, status):
        """Imprime o status do bot"""
        timestamp = status.get('timestamp', 'N/A')
        
        if status.get('bot_active'):
            print(f"🟢 [{timestamp}] Bot ativo: @{status['bot_username']}")
            if status.get('webhook_active'):
                print(f"   ⚠️ Webhook ativo: {status['webhook_url']}")
            if status.get('pending_updates', 0) > 0:
                print(f"   📨 {status['pending_updates']} updates pendentes")
        else:
            if status.get('conflict_detected'):
                print(f"🔴 [{timestamp}] CONFLITO DETECTADO!")
                print(f"   ❌ {status.get('error', 'Erro desconhecido')}")
            else:
                print(f"🟡 [{timestamp}] Bot inativo")
                print(f"   ❌ {status.get('error', 'Erro desconhecido')}")
                if status.get('consecutive_failures', 0) > 0:
                    print(f"   🔄 Falhas consecutivas: {status['consecutive_failures']}")
    
    async def run_monitor(self):
        """Executa o monitoramento contínuo"""
        if not await self.initialize():
            return
        
        self.running = True
        print("🔍 Monitor de saúde iniciado")
        print("📊 Verificando status a cada 30 segundos")
        print("🛑 Pressione Ctrl+C para parar")
        print("-" * 50)
        
        try:
            while self.running:
                status = await self.check_bot_health()
                self.print_status(status)
                
                # Se detectou conflito, tenta resolver
                if status.get('conflict_detected'):
                    print("🚨 Conflito detectado! Tentando resolver...")
                    if await self.resolve_conflict():
                        print("✅ Conflito resolvido! Continue monitorando...")
                    else:
                        print("❌ Falha ao resolver conflito automaticamente")
                        print("💡 Execute 'python fix_conflict.py' para limpeza manual")
                
                # Se muitas falhas consecutivas, sugere ação
                elif status.get('consecutive_failures', 0) >= self.max_failures:
                    print("⚠️ Muitas falhas consecutivas detectadas")
                    print("💡 Verifique sua conexão com a internet")
                
                # Aguarda próxima verificação
                await asyncio.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitor interrompido pelo usuário")
        except Exception as e:
            print(f"❌ Erro inesperado no monitor: {e}")
        finally:
            self.running = False
            print("👋 Monitor finalizado")

async def main():
    """Função principal"""
    print("🚛 RoteiroBot - Monitor de Saúde")
    print("=" * 50)
    
    monitor = BotMonitor()
    await monitor.run_monitor()

if __name__ == '__main__':
    asyncio.run(main())
