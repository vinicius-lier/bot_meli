#!/usr/bin/env python3
"""
RoteiroBot - Bot do Telegram para controle de rotas
Sistema de registro e consulta de rotas com cálculo automático de valores
"""

import logging
import asyncio
import signal
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from telegram.error import Conflict, NetworkError, TimedOut
from config import TELEGRAM_BOT_TOKEN
from db import init_database
from handlers import (
    start, help_command, rota_start, rota_data, rota_nome, rota_carro, 
    rota_ilha, rota_cancel, espelho_command, hoje_command, todas_command, 
    deletar_command, DATA, ROTA, CARRO, ILHA
)

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class RoteiroBot:
    """Classe principal do RoteiroBot com tratamento robusto de erros"""
    
    def __init__(self):
        self.application = None
        self.running = False
        self.restart_count = 0
        self.max_restarts = 5
        
    async def setup_application(self):
        """Configura a aplicação do bot"""
        # Cria a aplicação do bot
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Handler para o comando /rota (conversa)
        rota_handler = ConversationHandler(
            entry_points=[CommandHandler("rota", rota_start)],
            states={
                DATA: [MessageHandler(filters.TEXT & ~filters.COMMAND, rota_data)],
                ROTA: [MessageHandler(filters.TEXT & ~filters.COMMAND, rota_nome)],
                CARRO: [MessageHandler(filters.TEXT & ~filters.COMMAND, rota_carro)],
                ILHA: [MessageHandler(filters.TEXT & ~filters.COMMAND, rota_ilha)],
            },
            fallbacks=[CommandHandler("cancel", rota_cancel)],
        )
        
        # Adiciona os handlers
        self.application.add_handler(CommandHandler("start", start))
        self.application.add_handler(CommandHandler("help", help_command))
        self.application.add_handler(rota_handler)
        self.application.add_handler(CommandHandler("espelho", espelho_command))
        self.application.add_handler(CommandHandler("hoje", hoje_command))
        self.application.add_handler(CommandHandler("todas", todas_command))
        self.application.add_handler(CommandHandler("deletar", deletar_command))
    
    async def cleanup_bot_state(self):
        """Limpa completamente o estado do bot"""
        try:
            print("🧹 Limpando estado do bot...")
            
            # 1. Remove webhook
            await self.application.bot.delete_webhook(drop_pending_updates=True)
            
            # 2. Aguarda um pouco
            await asyncio.sleep(3)
            
            # 3. Limpa updates pendentes de forma mais agressiva
            try:
                # Tenta obter updates para limpar a fila
                updates = await self.application.bot.get_updates(limit=100, timeout=1)
                if updates:
                    print(f"📨 Limpando {len(updates)} updates pendentes...")
                    # Processa todos os updates para limpar a fila
                    for update in updates:
                        try:
                            await self.application.bot.get_updates(
                                offset=update.update_id + 1, 
                                limit=1, 
                                timeout=1
                            )
                        except:
                            pass
            except Exception as e:
                logger.warning(f"Erro ao limpar updates: {e}")
            
            # 4. Aguarda mais um pouco
            await asyncio.sleep(2)
            
            print("✅ Estado do bot limpo com sucesso")
            
        except Exception as e:
            logger.warning(f"Erro durante limpeza: {e}")

    async def start_bot(self):
        """Inicia o bot com tratamento robusto de erros"""
        self.running = True
        
        while self.running and self.restart_count < self.max_restarts:
            try:
                logger.info("Iniciando RoteiroBot...")
                print("🚛 RoteiroBot iniciado com sucesso!")
                print("📱 Bot está online e pronto para receber comandos")
                print("🛑 Pressione Ctrl+C para parar o bot")
                
                # Limpeza completa do estado antes de iniciar
                await self.cleanup_bot_state()
                
                # Inicia o polling com configurações otimizadas
                await self.application.run_polling(
                    allowed_updates=Update.ALL_TYPES,
                    drop_pending_updates=True,
                    close_loop=False,
                    read_timeout=30,
                    write_timeout=30,
                    connect_timeout=30,
                    pool_timeout=30
                )
                
            except Conflict as e:
                logger.error(f"Conflito detectado: {e}")
                print(f"⚠️ Conflito detectado: Múltiplas instâncias do bot detectadas")
                print("🔄 Tentando resolver conflito com limpeza agressiva...")
                
                # Limpeza agressiva do estado
                await self.cleanup_bot_state()
                
                self.restart_count += 1
                if self.restart_count < self.max_restarts:
                    wait_time = min(10 * self.restart_count, 60)  # Backoff mais longo
                    print(f"⏳ Aguardando {wait_time} segundos antes de tentar novamente...")
                    await asyncio.sleep(wait_time)
                else:
                    print("❌ Máximo de tentativas de reinicialização atingido")
                    print("💡 Execute 'python fix_conflict.py' para limpeza manual")
                    break
                    
            except (NetworkError, TimedOut) as e:
                logger.error(f"Erro de rede: {e}")
                print(f"🌐 Erro de rede: {e}")
                print("🔄 Tentando reconectar...")
                
                self.restart_count += 1
                if self.restart_count < self.max_restarts:
                    wait_time = min(10 * self.restart_count, 60)
                    print(f"⏳ Aguardando {wait_time} segundos...")
                    await asyncio.sleep(wait_time)
                else:
                    print("❌ Máximo de tentativas de reconexão atingido")
                    break
                    
            except KeyboardInterrupt:
                logger.info("Bot interrompido pelo usuário")
                print("\n🛑 Bot interrompido pelo usuário")
                self.running = False
                break
                
            except Exception as e:
                logger.error(f"Erro inesperado: {e}")
                print(f"❌ Erro inesperado: {e}")
                
                self.restart_count += 1
                if self.restart_count < self.max_restarts:
                    wait_time = min(5 * self.restart_count, 30)
                    print(f"🔄 Tentando reiniciar em {wait_time} segundos...")
                    await asyncio.sleep(wait_time)
                else:
                    print("❌ Máximo de tentativas de reinicialização atingido")
                    break
    
    async def stop_bot(self):
        """Para o bot de forma segura"""
        self.running = False
        if self.application:
            await self.application.stop()
            await self.application.shutdown()

def signal_handler(signum, frame):
    """Handler para sinais do sistema"""
    print(f"\n🛑 Sinal {signum} recebido. Parando o bot...")
    sys.exit(0)

async def main():
    """Função principal que inicia o bot"""
    
    # Configura handlers de sinal
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Verifica se o token foi configurado
    if not TELEGRAM_BOT_TOKEN:
        logger.error("Token do Telegram não configurado!")
        print("❌ ERRO: Token do Telegram não encontrado!")
        print("📝 Crie um arquivo .env com: TELEGRAM_BOT_TOKEN=seu_token_aqui")
        print("🔗 Obtenha seu token em: https://t.me/BotFather")
        return
    
    # Inicializa o banco de dados
    try:
        init_database()
        logger.info("Banco de dados inicializado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {e}")
        print(f"❌ Erro ao inicializar banco de dados: {e}")
        return
    
    # Cria e inicia o bot
    bot = RoteiroBot()
    await bot.setup_application()
    await bot.start_bot()
    await bot.stop_bot()

if __name__ == '__main__':
    asyncio.run(main())