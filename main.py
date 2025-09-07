#!/usr/bin/env python3
"""
RoteiroBot - Bot do Telegram para controle de rotas
Sistema de registro e consulta de rotas com cálculo automático de valores
"""

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
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

def main():
    """Função principal que inicia o bot"""
    
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
    
    # Cria a aplicação do bot

    
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
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
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(rota_handler)
    application.add_handler(CommandHandler("espelho", espelho_command))
    application.add_handler(CommandHandler("hoje", hoje_command))
    application.add_handler(CommandHandler("todas", todas_command))
    application.add_handler(CommandHandler("deletar", deletar_command))
    
    # Inicia o bot
    logger.info("Iniciando RoteiroBot...")
    print("🚛 RoteiroBot iniciado com sucesso!")
    print("📱 Bot está online e pronto para receber comandos")
    print("🛑 Pressione Ctrl+C para parar o bot")
    
    try:
        # Inicia o polling
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
    except KeyboardInterrupt:
        logger.info("Bot interrompido pelo usuário")
        print("\n🛑 Bot interrompido pelo usuário")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        print(f"❌ Erro inesperado: {e}")

if __name__ == '__main__':
    main()