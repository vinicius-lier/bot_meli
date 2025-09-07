import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
try:
    load_dotenv()
except:
    pass

# Token do Bot do Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Se não conseguir carregar do .env, tenta carregar diretamente
if not TELEGRAM_BOT_TOKEN:
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if 'TELEGRAM_BOT_TOKEN=' in content:
                TELEGRAM_BOT_TOKEN = content.split('TELEGRAM_BOT_TOKEN=')[1]
    except:
        pass

# Para ambiente de produção (nuvem), usa variável de ambiente diretamente
if not TELEGRAM_BOT_TOKEN:
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not TELEGRAM_BOT_TOKEN:
    print("⚠️  AVISO: Token do Telegram não encontrado!")
    print("Configure a variável de ambiente TELEGRAM_BOT_TOKEN")
    print("Obtenha seu token em: https://t.me/BotFather")