<<<<<<< HEAD
# 🚛 RoteiroBot

Bot do Telegram para controle de rotas com cálculo automático de valores.

## 📋 Funcionalidades

- **Registrar rotas** com comando `/rota`
- **Consultar espelho de pagamento** com comando `/espelho [data_inicial] [data_final]`
- **Ver rotas de hoje** com comando `/hoje`
- **Listar todas as rotas** com comando `/todas`
- **Deletar rota** com comando `/deletar [id]`

## 💰 Sistema de Valores

- **Van**: R$ 130,00
- **Fiorino**: R$ 110,00
- **Entrega em ilha**: +R$ 10,00

## 🚀 Como Usar

### 1. Pré-requisitos

- Python 3.8 ou superior
- Token do Bot do Telegram

### 2. Instalação

1. Navegue até a pasta do projeto:
   ```bash
   cd "C:\Users\vinny\OneDrive\Desktop\VINICIUS\Bot Telegram\RoteiroBot"
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuração

1. Crie um arquivo `.env` na pasta do projeto:
   ```bash
   # No Windows PowerShell
   echo TELEGRAM_BOT_TOKEN=seu_token_aqui > .env
   ```

2. **Obtenha seu token do Bot:**
   - Acesse [@BotFather](https://t.me/BotFather) no Telegram
   - Digite `/newbot`
   - Siga as instruções para criar seu bot
   - Copie o token fornecido
   - Substitua `seu_token_aqui` no arquivo `.env` pelo token real

### 4. Executar o Bot

```bash
python main.py
```

Se tudo estiver correto, você verá:
```
🚛 RoteiroBot iniciado com sucesso!
📱 Bot está online e pronto para receber comandos
🛑 Pressione Ctrl+C para parar o bot
```

## 📱 Como Usar no Telegram

### Comandos Disponíveis

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `/start` | Inicia o bot e mostra ajuda | `/start` |
| `/help` | Mostra ajuda detalhada | `/help` |
| `/rota` | Registra nova rota | `/rota` |
| `/espelho` | Consulta espelho de pagamento | `/espelho 01/09/2025 07/09/2025` |
| `/hoje` | Mostra rotas de hoje | `/hoje` |
| `/todas` | Lista todas as rotas | `/todas` |
| `/deletar` | Remove rota por ID | `/deletar 5` |

### Exemplo de Uso Completo

#### 1. Registrar uma Rota
```
Usuário: /rota
Bot: Qual a data da rota?
Usuário: 07/09/2025
Bot: Qual o nome da rota?
Usuário: P10-AM
Bot: Qual o carro usado? (Van ou Fiorino)
Usuário: Van
Bot: Teve entrega em ilha? (Sim ou Não)
Usuário: Sim
Bot: ✅ Rota registrada! Valor: R$ 140,00
```

#### 2. Consultar Espelho de Pagamento
```
Usuário: /espelho 01/09/2025 07/09/2025
Bot: 
📅 Período: 01/09/2025 até 07/09/2025

• 01/09/2025 | P10-AM | Van | Ilha | R$ 140,00
• 02/09/2025 | G20-PM | Fiorino | Sem ilha | R$ 110,00
• 05/09/2025 | I7-AM | Van | Sem ilha | R$ 130,00

💰 Total no período: R$ 380,00
```

## 🗄️ Banco de Dados

O bot usa SQLite e cria automaticamente o arquivo `rotas.db` com a seguinte estrutura:

```sql
CREATE TABLE rotas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    rota TEXT NOT NULL,
    carro TEXT NOT NULL,
    ilha INTEGER NOT NULL,
    valor REAL NOT NULL
);
```

## 📁 Estrutura do Projeto

```
RoteiroBot/
├── main.py              # Arquivo principal do bot
├── db.py                # Funções de banco de dados
├── handlers.py          # Handlers dos comandos
├── config.py            # Configurações e variáveis de ambiente
├── requirements.txt     # Dependências do projeto
├── README.md           # Este arquivo
└── rotas.db            # Banco de dados (criado automaticamente)
```

## 🔧 Solução de Problemas

### Erro: "Token do Telegram não encontrado"
- Verifique se o arquivo `.env` existe
- Confirme se o token está correto no arquivo `.env`
- Certifique-se de que não há espaços extras no token

### Erro: "ModuleNotFoundError"
- Execute: `pip install -r requirements.txt`
- Verifique se está usando Python 3.8+

### Bot não responde
- Verifique se o bot está rodando (terminal deve mostrar "Bot está online")
- Confirme se o token está correto
- Teste enviando `/start` para o bot

## 📝 Logs

O bot gera logs detalhados no terminal. Para parar o bot, pressione `Ctrl+C`.

## 🤝 Contribuição

Sinta-se à vontade para contribuir com melhorias, correções de bugs ou novas funcionalidades!

## 📄 Licença

Este projeto é de uso livre para fins educacionais e comerciais.
=======
# bot_meli
>>>>>>> 3d86cf3eb756a6dac1e2e9de52bedee5ef128976
