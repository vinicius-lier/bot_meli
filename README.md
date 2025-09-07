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

**🚀 MÉTODO DEFINITIVO (Recomendado):**
```bash
python run_bot.py
```
*Este método inclui limpeza automática de conflitos e inicialização robusta*

**Método Alternativo (Inicialização Segura):**
```bash
python start_bot.py
```

**Método Básico:**
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
├── run_bot.py           # 🚀 Script de execução definitivo (RECOMENDADO)
├── main.py              # Arquivo principal do bot (versão robusta)
├── start_bot.py         # Script de inicialização segura
├── fix_conflict.py      # Script para resolver conflitos
├── monitor_bot.py       # Monitor de saúde contínuo
├── db.py                # Funções de banco de dados
├── handlers.py          # Handlers dos comandos
├── config.py            # Configurações e variáveis de ambiente
├── requirements.txt     # Dependências do projeto
├── README.md           # Este arquivo
├── .env                # Arquivo de configuração (criar manualmente)
└── rotas.db            # Banco de dados (criado automaticamente)
```

## 🔧 Solução de Problemas

### ❌ Erro: "Conflict: terminated by other getUpdates request"

Este é o erro mais comum e indica múltiplas instâncias do bot rodando simultaneamente.

**🚀 Solução Definitiva (Recomendada):**
```bash
python run_bot.py
```
*Este script resolve conflitos automaticamente antes de iniciar*

**Solução Rápida:**
```bash
python fix_conflict.py
```

**Solução Manual:**
1. Pare todas as instâncias do bot (Ctrl+C em todos os terminais)
2. Execute: `python fix_conflict.py`
3. Escolha a opção "1" para resolver conflitos
4. Inicie o bot novamente: `python run_bot.py`

**Monitoramento Contínuo:**
```bash
python monitor_bot.py
```
*Para monitorar a saúde do bot em tempo real*

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

### Bot reinicia constantemente
- Use `python run_bot.py` (método definitivo)
- Execute `python fix_conflict.py` para limpar conflitos
- Use `python monitor_bot.py` para monitorar em tempo real
- Verifique sua conexão com a internet

### Bot não inicia após conflito
- Execute `python fix_conflict.py` e escolha opção "1"
- Aguarde 30 segundos antes de tentar novamente
- Use `python run_bot.py` para inicialização robusta

## 📝 Logs

O bot gera logs detalhados no terminal. Para parar o bot, pressione `Ctrl+C`.

## 🤝 Contribuição

Sinta-se à vontade para contribuir com melhorias, correções de bugs ou novas funcionalidades!

## 📄 Licença

Este projeto é de uso livre para fins educacionais e comerciais.
