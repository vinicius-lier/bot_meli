#!/usr/bin/env python3
"""
Script de Execução Definitivo do RoteiroBot
Combina todas as melhorias para uma execução robusta e livre de conflitos
"""

import asyncio
import logging
import sys
import os
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

class UltimateBotRunner:
    """Executor definitivo do bot com todas as proteções"""
    
    def __init__(self):
        self.bot = None
        self.startup_time = datetime.now()
        
    async def pre_startup_cleanup(self):
        """Limpeza completa antes de iniciar o bot"""
        print("🚀 RoteiroBot - Inicialização Definitiva")
        print("=" * 60)
        print(f"⏰ Iniciado em: {self.startup_time.strftime('%d/%m/%Y %H:%M:%S')}")
        print()
        
        if not TELEGRAM_BOT_TOKEN:
            print("❌ ERRO: Token do Telegram não encontrado!")
            print("📝 Configure a variável TELEGRAM_BOT_TOKEN no arquivo .env")
            return False
        
        try:
            print("🔍 Verificando e limpando estado do bot...")
            self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
            
            # 1. Verifica se o bot responde
            try:
                bot_info = await self.bot.get_me()
                print(f"✅ Bot verificado: @{bot_info.username}")
            except Conflict:
                print("⚠️ Conflito detectado! Iniciando limpeza...")
                
                # 2. Limpeza agressiva
                await self.aggressive_cleanup()
                
                # 3. Verifica novamente
                try:
                    bot_info = await self.bot.get_me()
                    print(f"✅ Conflito resolvido! Bot: @{bot_info.username}")
                except Conflict:
                    print("❌ Conflito persistente após limpeza")
                    print("💡 Execute 'python fix_conflict.py' para limpeza manual")
                    return False
            
            # 4. Limpeza preventiva
            await self.preventive_cleanup()
            
            print("✅ Estado do bot limpo e pronto para inicialização")
            return True
            
        except Exception as e:
            print(f"❌ Erro durante verificação: {e}")
            return False
    
    async def aggressive_cleanup(self):
        """Limpeza agressiva do estado do bot"""
        print("🧹 Executando limpeza agressiva...")
        
        try:
            # Remove webhook
            await self.bot.delete_webhook(drop_pending_updates=True)
            print("   📡 Webhook removido")
            
            # Aguarda
            await asyncio.sleep(3)
            
            # Limpa updates pendentes
            total_cleaned = 0
            for attempt in range(3):
                try:
                    updates = await self.bot.get_updates(limit=100, timeout=1)
                    if updates:
                        print(f"   📨 Tentativa {attempt + 1}: {len(updates)} updates")
                        for update in updates:
                            try:
                                await self.bot.get_updates(
                                    offset=update.update_id + 1, 
                                    limit=1, 
                                    timeout=1
                                )
                                total_cleaned += 1
                            except:
                                pass
                        await asyncio.sleep(2)
                    else:
                        break
                except Exception as e:
                    print(f"   ⚠️ Erro na tentativa {attempt + 1}: {e}")
                    await asyncio.sleep(2)
            
            if total_cleaned > 0:
                print(f"   ✅ {total_cleaned} updates limpos")
            
            await asyncio.sleep(2)
            print("   ✅ Limpeza agressiva concluída")
            
        except Exception as e:
            print(f"   ❌ Erro durante limpeza: {e}")
    
    async def preventive_cleanup(self):
        """Limpeza preventiva antes de iniciar"""
        print("🛡️ Executando limpeza preventiva...")
        
        try:
            # Remove webhook preventivamente
            await self.bot.delete_webhook(drop_pending_updates=True)
            
            # Limpa updates pendentes
            updates = await self.bot.get_updates(limit=10, timeout=1)
            if updates:
                print(f"   📨 {len(updates)} updates preventivos limpos")
                for update in updates:
                    try:
                        await self.bot.get_updates(
                            offset=update.update_id + 1, 
                            limit=1, 
                            timeout=1
                        )
                    except:
                        pass
            
            await asyncio.sleep(1)
            print("   ✅ Limpeza preventiva concluída")
            
        except Exception as e:
            print(f"   ⚠️ Erro na limpeza preventiva: {e}")
    
    async def start_bot(self):
        """Inicia o bot principal"""
        print()
        print("🚛 Iniciando RoteiroBot...")
        print("📱 Bot estará online em instantes...")
        print("🛑 Pressione Ctrl+C para parar")
        print("-" * 60)
        
        try:
            # Importa e executa o main
            from main import main
            await main()
            return True
            
        except KeyboardInterrupt:
            print("\n🛑 Bot interrompido pelo usuário")
            return True
        except Exception as e:
            print(f"❌ Erro ao iniciar bot: {e}")
            logger.error(f"Erro ao iniciar bot: {e}")
            return False
    
    async def run(self):
        """Executa o processo completo"""
        # 1. Limpeza pré-inicialização
        if not await self.pre_startup_cleanup():
            print("\n❌ Falha na verificação inicial. Abortando.")
            return False
        
        # 2. Inicia o bot
        print()
        success = await self.start_bot()
        
        if success:
            print("\n✅ Bot finalizado com sucesso")
        else:
            print("\n❌ Bot finalizado com erro")
            print("\n💡 Dicas para resolver problemas:")
            print("1. Execute: python fix_conflict.py")
            print("2. Verifique sua conexão com a internet")
            print("3. Certifique-se de que não há outras instâncias rodando")
        
        return success

async def main():
    """Função principal"""
    runner = UltimateBotRunner()
    await runner.run()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Execução interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)
