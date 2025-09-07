#!/usr/bin/env python3
"""
Script para resolver conflitos de múltiplas instâncias do bot
Este script limpa webhooks e updates pendentes do Telegram
"""

import asyncio
import logging
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def fix_bot_conflict():
    """Resolve conflitos de múltiplas instâncias do bot"""
    
    if not TELEGRAM_BOT_TOKEN:
        print("❌ ERRO: Token do Telegram não encontrado!")
        print("📝 Configure a variável TELEGRAM_BOT_TOKEN")
        return False
    
    try:
        # Cria instância do bot
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        print("🔧 Iniciando correção agressiva de conflitos...")
        
        # 1. Remove webhook se existir
        print("📡 Removendo webhook...")
        await bot.delete_webhook(drop_pending_updates=True)
        
        # 2. Aguarda um pouco
        print("⏳ Aguardando 3 segundos...")
        await asyncio.sleep(3)
        
        # 3. Limpa updates pendentes de forma mais agressiva
        print("🧹 Limpando updates pendentes...")
        total_cleaned = 0
        
        # Múltiplas tentativas de limpeza
        for attempt in range(3):
            try:
                updates = await bot.get_updates(limit=100, timeout=1)
                if updates:
                    print(f"📨 Tentativa {attempt + 1}: {len(updates)} updates encontrados")
                    
                    # Processa todos os updates para limpar a fila
                    for update in updates:
                        try:
                            await bot.get_updates(
                                offset=update.update_id + 1, 
                                limit=1, 
                                timeout=1
                            )
                            total_cleaned += 1
                        except Exception as e:
                            logger.warning(f"Erro ao processar update {update.update_id}: {e}")
                    
                    # Aguarda entre tentativas
                    if attempt < 2:
                        await asyncio.sleep(2)
                else:
                    print(f"✅ Tentativa {attempt + 1}: Nenhum update pendente")
                    break
                    
            except Exception as e:
                print(f"⚠️ Erro na tentativa {attempt + 1}: {e}")
                if attempt < 2:
                    await asyncio.sleep(2)
        
        if total_cleaned > 0:
            print(f"✅ Total de {total_cleaned} updates limpos")
        else:
            print("✅ Nenhum update pendente encontrado")
        
        # 4. Aguarda mais um pouco
        print("⏳ Aguardando 2 segundos...")
        await asyncio.sleep(2)
        
        # 5. Verifica informações do bot
        print("🤖 Verificando informações do bot...")
        bot_info = await bot.get_me()
        print(f"✅ Bot conectado: @{bot_info.username} ({bot_info.first_name})")
        
        # 6. Verificação final
        print("🔍 Verificação final...")
        final_updates = await bot.get_updates(limit=1, timeout=1)
        if final_updates:
            print(f"⚠️ Ainda há {len(final_updates)} updates pendentes")
            print("💡 Pode ser necessário aguardar mais tempo ou reiniciar o bot")
        else:
            print("✅ Nenhum update pendente - sistema limpo!")
        
        print("🎉 Correção de conflitos concluída!")
        print("🚀 Agora você pode iniciar o bot normalmente")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao resolver conflitos: {e}")
        logger.error(f"Erro ao resolver conflitos: {e}")
        return False

async def check_bot_status():
    """Verifica o status atual do bot"""
    
    if not TELEGRAM_BOT_TOKEN:
        print("❌ ERRO: Token do Telegram não encontrado!")
        return False
    
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        print("🔍 Verificando status do bot...")
        
        # Verifica informações do bot
        bot_info = await bot.get_me()
        print(f"✅ Bot ativo: @{bot_info.username} ({bot_info.first_name})")
        
        # Verifica webhook
        webhook_info = await bot.get_webhook_info()
        if webhook_info.url:
            print(f"⚠️ Webhook ativo: {webhook_info.url}")
            print("💡 Use este script para remover o webhook se necessário")
        else:
            print("✅ Nenhum webhook ativo")
        
        # Verifica updates pendentes
        updates = await bot.get_updates(limit=1, timeout=1)
        if updates:
            print(f"⚠️ {len(updates)} updates pendentes encontrados")
        else:
            print("✅ Nenhum update pendente")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar status: {e}")
        return False

async def main():
    """Função principal"""
    print("🚛 RoteiroBot - Resolvedor de Conflitos")
    print("=" * 50)
    
    while True:
        print("\n📋 Opções disponíveis:")
        print("1. Resolver conflitos (recomendado)")
        print("2. Verificar status do bot")
        print("3. Sair")
        
        try:
            choice = input("\n🔢 Escolha uma opção (1-3): ").strip()
            
            if choice == "1":
                print("\n🔧 Resolvendo conflitos...")
                success = await fix_bot_conflict()
                if success:
                    print("\n✅ Conflitos resolvidos! Você pode iniciar o bot agora.")
                else:
                    print("\n❌ Falha ao resolver conflitos. Verifique o token.")
                    
            elif choice == "2":
                print("\n🔍 Verificando status...")
                await check_bot_status()
                
            elif choice == "3":
                print("\n👋 Saindo...")
                break
                
            else:
                print("❌ Opção inválida! Escolha 1, 2 ou 3.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Saindo...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == '__main__':
    asyncio.run(main())
