#!/usr/bin/env python3
"""
Script para limpar updates pendentes do bot do Telegram
Execute este script quando houver erro HTTP 409 Conflict
"""

import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

async def limpar_updates():
    """Limpa todos os updates pendentes do bot"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ Token do Telegram não encontrado!")
        return
    
    bot = Bot(token=token)
    
    try:
        # Obtém updates pendentes
        updates = await bot.get_updates()
        print(f"📥 Encontrados {len(updates)} updates pendentes")
        
        if updates:
            # Obtém o ID do último update
            last_update_id = updates[-1].update_id
            print(f"🔄 Limpando updates até ID: {last_update_id}")
            
            # Limpa os updates
            await bot.get_updates(offset=last_update_id + 1)
            print("✅ Updates limpos com sucesso!")
        else:
            print("✅ Nenhum update pendente encontrado")
            
    except Exception as e:
        print(f"❌ Erro ao limpar updates: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    print("🧹 Limpando updates pendentes do bot...")
    asyncio.run(limpar_updates())
    print("🎉 Processo concluído!")
