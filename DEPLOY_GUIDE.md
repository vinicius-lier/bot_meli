# 🚀 Guia de Deploy - RoteiroBot na Nuvem

## 🌐 Opções de Hospedagem GRATUITAS

### 1. Railway (RECOMENDADO) ⭐

**Vantagens:**
- ✅ Gratuito com 500 horas/mês
- ✅ Deploy automático via GitHub
- ✅ Banco de dados SQLite incluído
- ✅ Interface simples

**Como fazer:**

1. **Criar conta no Railway:**
   - Acesse: https://railway.app
   - Faça login com GitHub

2. **Preparar o repositório:**
   ```bash
   # No seu projeto, execute:
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/roteiro-bot.git
   git push -u origin main
   ```

3. **Deploy no Railway:**
   - Clique em "New Project"
   - Selecione "Deploy from GitHub repo"
   - Escolha seu repositório
   - Railway detectará automaticamente que é Python

4. **Configurar variáveis:**
   - Vá em "Variables"
   - Adicione: `TELEGRAM_BOT_TOKEN` = seu_token_aqui

5. **Deploy:**
   - Railway fará o deploy automaticamente
   - O bot ficará online 24/7!

---

### 2. Render

**Como fazer:**

1. **Criar conta:** https://render.com
2. **Conectar GitHub**
3. **Criar novo Web Service**
4. **Configurar:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
   - Environment: `TELEGRAM_BOT_TOKEN=seu_token`

---

### 3. PythonAnywhere

**Como fazer:**

1. **Criar conta:** https://pythonanywhere.com
2. **Upload dos arquivos**
3. **Configurar Web App**
4. **Adicionar variável de ambiente**

---

## 🔧 Arquivos Necessários (já criados)

- ✅ `requirements.txt` - Dependências Python
- ✅ `Procfile` - Para Heroku/Railway
- ✅ `railway.json` - Configuração Railway
- ✅ `runtime.txt` - Versão Python
- ✅ `config.py` - Atualizado para nuvem

---

## 🚨 IMPORTANTE

1. **Token do Bot:**
   - Obtenha em: https://t.me/BotFather
   - Configure como variável de ambiente (NÃO no código)

2. **Banco de Dados:**
   - SQLite funciona perfeitamente na nuvem
   - Dados persistem entre reinicializações

3. **Logs:**
   - Use a interface da plataforma para ver logs
   - Railway: Dashboard > Logs
   - Render: Dashboard > Logs

---

## 🎯 Recomendação Final

**Use Railway** - É a opção mais simples e confiável para bots do Telegram!

1. Crie conta no Railway
2. Conecte seu GitHub
3. Deploy automático
4. Configure o token
5. Bot online 24/7! 🎉
