#!/usr/bin/env python3
"""
Script de inicialização robusta do RoteiroBot
Inclui verificação de conflitos e inicialização segura
"""

import asyncio
import logging
import sys
import os
from telegram import Bot
from telegram.error import Conflict
from config import TELEGRAM_BOT_TOKEN

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def check_and_fix_conflicts():
    """Verifica e resolve conflitos antes de iniciar o bot"""
    
    if not TELEGRAM_BOT_TOKEN:
        print("❌ ERRO: Token do Telegram não encontrado!")
        return False
    
    try:
        print("🔍 Verificando conflitos...")
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        # Tenta obter informações do bot
        try:
            bot_info = await bot.get_me()
            print(f"✅ Bot verificado: @{bot_info.username}")
        except Conflict:
            print("⚠️ Conflito detectado! Resolvendo...")
            
            # Remove webhook e limpa updates
            await bot.delete_webhook(drop_pending_updates=True)
            print("🧹 Webhook removido e updates limpos")
            
            # Aguarda um pouco
            await asyncio.sleep(2)
            
            # Verifica novamente
            try:
                bot_info = await bot.get_me()
                print(f"✅ Conflito resolvido! Bot: @{bot_info.username}")
            except Conflict:
                print("❌ Conflito persistente. Execute fix_conflict.py manualmente.")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar conflitos: {e}")
        return False

async def start_bot_safely():
    """Inicia o bot de forma segura"""
    
    print("🚛 RoteiroBot - Inicialização Segura")
    print("=" * 50)
    
    # Verifica se o token está configurado
    if not TELEGRAM_BOT_TOKEN:
        print("❌ ERRO: Token do Telegram não configurado!")
        print("📝 Configure a variável TELEGRAM_BOT_TOKEN no arquivo .env")
        print("🔗 Obtenha seu token em: https://t.me/BotFather")
        return False
    
    # Verifica e resolve conflitos
    if not await check_and_fix_conflicts():
        print("❌ Não foi possível resolver conflitos. Abortando inicialização.")
        return False
    
    print("✅ Verificações concluídas com sucesso!")
    print("🚀 Iniciando bot...")
    
    # Importa e executa o main
    try:
        from main import main
        await main()
        return True
    except Exception as e:
        print(f"❌ Erro ao iniciar bot: {e}")
        logger.error(f"Erro ao iniciar bot: {e}")
        return False

def main():
    """Função principal"""
    try:
        # Executa a inicialização segura
        success = asyncio.run(start_bot_safely())
        
        if not success:
            print("\n💡 Dicas para resolver problemas:")
            print("1. Execute: python fix_conflict.py")
            print("2. Verifique se o token está correto")
            print("3. Certifique-se de que não há outras instâncias rodando")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Inicialização interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
