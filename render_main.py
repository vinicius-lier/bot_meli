#!/usr/bin/env python3
"""
RoteiroBot - Versão Otimizada para Render
Bot do Telegram para controle de rotas com cálculo automático de valores
Versão simplificada e robusta para deploy em produção
"""

import logging
import asyncio
import signal
import sys
import os
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

class RenderBot:
    """Classe do bot otimizada para Render"""
    
    def __init__(self):
        self.application = None
        self.running = False
        self.restart_count = 0
        self.max_restarts = 3  # Menos tentativas para Render
        
    async def setup_application(self):
        """Configura a aplicação do bot"""
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
    
    async def cleanup_for_render(self):
        """Limpeza otimizada para Render"""
        try:
            logger.info("Limpando estado do bot para Render...")
            
            # Remove webhook
            await self.application.bot.delete_webhook(drop_pending_updates=True)
            logger.info("Webhook removido")
            
            # Aguarda um pouco
            await asyncio.sleep(2)
            
            # Limpa updates pendentes de forma simples
            try:
                updates = await self.application.bot.get_updates(limit=50, timeout=1)
                if updates:
                    logger.info(f"Limpando {len(updates)} updates pendentes")
                    # Processa updates para limpar a fila
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
            
            await asyncio.sleep(1)
            logger.info("Limpeza concluída")
            
        except Exception as e:
            logger.warning(f"Erro durante limpeza: {e}")
    
    async def start_bot(self):
        """Inicia o bot com tratamento robusto para Render"""
        self.running = True
        
        while self.running and self.restart_count < self.max_restarts:
            try:
                logger.info("Iniciando RoteiroBot no Render...")
                print("🚛 RoteiroBot iniciado com sucesso!")
                print("📱 Bot está online e pronto para receber comandos")
                
                # Limpeza antes de iniciar
                await self.cleanup_for_render()
                
                # Inicia o polling com configurações básicas
                await self.application.run_polling(
                    allowed_updates=Update.ALL_TYPES,
                    drop_pending_updates=True,
                    close_loop=False
                )
                
            except Conflict as e:
                logger.error(f"Conflito detectado: {e}")
                print(f"⚠️ Conflito detectado - resolvendo...")
                
                # Limpeza agressiva
                await self.cleanup_for_render()
                
                self.restart_count += 1
                if self.restart_count < self.max_restarts:
                    wait_time = 5 * self.restart_count
                    logger.info(f"Aguardando {wait_time} segundos...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error("Máximo de tentativas atingido")
                    break
                    
            except (NetworkError, TimedOut) as e:
                logger.error(f"Erro de rede: {e}")
                print(f"🌐 Erro de rede - tentando reconectar...")
                
                self.restart_count += 1
                if self.restart_count < self.max_restarts:
                    wait_time = 10 * self.restart_count
                    logger.info(f"Aguardando {wait_time} segundos...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error("Máximo de tentativas de reconexão atingido")
                    break
                    
            except Exception as e:
                logger.error(f"Erro inesperado: {e}")
                print(f"❌ Erro inesperado: {e}")
                
                self.restart_count += 1
                if self.restart_count < self.max_restarts:
                    wait_time = 5 * self.restart_count
                    logger.info(f"Tentando reiniciar em {wait_time} segundos...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error("Máximo de tentativas de reinicialização atingido")
                    break
    
    async def stop_bot(self):
        """Para o bot de forma segura"""
        self.running = False
        if self.application:
            await self.application.stop()
            await self.application.shutdown()

def signal_handler(signum, frame):
    """Handler para sinais do sistema"""
    logger.info(f"Sinal {signum} recebido. Parando o bot...")
    sys.exit(0)

async def main():
    """Função principal otimizada para Render"""
    
    # Configura handlers de sinal
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Verifica se o token foi configurado
    if not TELEGRAM_BOT_TOKEN:
        logger.error("Token do Telegram não configurado!")
        print("❌ ERRO: Token do Telegram não encontrado!")
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
    bot = RenderBot()
    await bot.setup_application()
    await bot.start_bot()
    await bot.stop_bot()

if __name__ == '__main__':
    asyncio.run(main())
