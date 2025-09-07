import re
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from db import (
    init_database, insert_rota, get_rotas_por_periodo, get_rotas_hoje, 
    get_todas_rotas, delete_rota, get_total_periodo, get_total_hoje
)

# Estados da conversa para o comando /rota
DATA, ROTA, CARRO, ILHA = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /start - Mensagem de boas-vindas"""
    welcome_message = """
🚛 *RoteiroBot* - Sistema de Controle de Rotas

*Comandos disponíveis:*
/rota - Registrar nova rota
/espelho [data_inicial] [data_final] - Consultar espelho de pagamento
/hoje - Ver rotas de hoje
/todas - Listar todas as rotas
/deletar [id] - Remover rota por ID
/help - Mostrar esta ajuda

*Exemplo de uso:*
/espelho 01/09/2025 07/09/2025
/deletar 5

Digite /rota para começar a registrar uma nova rota! 🚀
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /help - Mostra ajuda detalhada"""
    help_message = """
📋 *Ajuda do RoteiroBot*

*Comandos:*

🚛 `/rota` - Registrar nova rota
   • Pergunta: data, nome da rota, carro, se teve ilha
   • Calcula valor automaticamente

📊 `/espelho [data_inicial] [data_final]` - Espelho de pagamento
   • Exemplo: /espelho 01/09/2025 07/09/2025
   • Mostra rotas do período + total

📅 `/hoje` - Rotas de hoje
   • Lista todas as rotas da data atual

📋 `/todas` - Todas as rotas
   • Lista todas as rotas cadastradas

🗑️ `/deletar [id]` - Remover rota
   • Exemplo: /deletar 5

*Valores:*
• Van: R$ 130
• Fiorino: R$ 110
• +R$ 10 se teve entrega em ilha
    """
    await update.message.reply_text(help_message, parse_mode='Markdown')

async def rota_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicia o processo de registro de rota"""
    await update.message.reply_text(
        "🚛 *Registro de Nova Rota*\n\n"
        "Qual a data da rota?\n"
        "📅 Digite no formato DD/MM/AAAA ou 'hoje'",
        parse_mode='Markdown'
    )
    return DATA

async def rota_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa a data da rota"""
    data_input = update.message.text.strip()
    
    if data_input.lower() == "hoje":
        data = datetime.now().strftime("%d/%m/%Y")
    else:
        # Valida formato da data
        try:
            datetime.strptime(data_input, "%d/%m/%Y")
            data = data_input
        except ValueError:
            await update.message.reply_text(
                "❌ Formato de data inválido!\n"
                "📅 Use DD/MM/AAAA ou digite 'hoje'"
            )
            return DATA
    
    context.user_data['data'] = data
    
    await update.message.reply_text(
        f"📅 Data: {data}\n\n"
        "Qual o nome da rota?\n"
        "🚛 Exemplo: P10-AM, G20-PM, I7-AM"
    )
    return ROTA

async def rota_nome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa o nome da rota"""
    rota = update.message.text.strip()
    context.user_data['rota'] = rota
    
    await update.message.reply_text(
        f"🚛 Rota: {rota}\n\n"
        "Qual o carro usado?\n"
        "🚐 Digite: Van ou Fiorino"
    )
    return CARRO

async def rota_carro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa o tipo de carro"""
    carro = update.message.text.strip().lower()
    
    if carro not in ['van', 'fiorino']:
        await update.message.reply_text(
            "❌ Tipo de carro inválido!\n"
            "🚐 Digite: Van ou Fiorino"
        )
        return CARRO
    
    context.user_data['carro'] = carro.capitalize()
    
    await update.message.reply_text(
        f"🚐 Carro: {carro.capitalize()}\n\n"
        "Teve entrega em ilha?\n"
        "🏝️ Digite: Sim ou Não"
    )
    return ILHA

async def rota_ilha(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processa se teve entrega em ilha e finaliza o registro"""
    ilha_input = update.message.text.strip().lower()
    
    if ilha_input not in ['sim', 'não', 'nao', 's', 'n']:
        await update.message.reply_text(
            "❌ Resposta inválida!\n"
            "🏝️ Digite: Sim ou Não"
        )
        return ILHA
    
    ilha = ilha_input in ['sim', 's']
    
    # Salva no banco de dados
    try:
        rota_id = insert_rota(
            context.user_data['data'],
            context.user_data['rota'],
            context.user_data['carro'],
            ilha
        )
        
        # Calcula valor para exibição
        valor_base = 130 if context.user_data['carro'].lower() == "van" else 110
        valor_final = valor_base + (10 if ilha else 0)
        
        ilha_texto = "Sim" if ilha else "Não"
        
        await update.message.reply_text(
            f"✅ Rota registrada com sucesso!\n\n"
            f"🆔 ID: {rota_id}\n"
            f"📅 Data: {context.user_data['data']}\n"
            f"🚛 Rota: {context.user_data['rota']}\n"
            f"🚐 Carro: {context.user_data['carro']}\n"
            f"🏝️ Ilha: {ilha_texto}\n"
            f"💰 Valor: R$ {valor_final:.2f}"
        )
        
    except Exception as e:
        await update.message.reply_text(
            f"❌ Erro ao registrar rota: {str(e)}"
        )
    
    # Limpa dados da conversa
    context.user_data.clear()
    return ConversationHandler.END

async def rota_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela o registro de rota"""
    context.user_data.clear()
    await update.message.reply_text("❌ Registro de rota cancelado.")
    return ConversationHandler.END

async def espelho_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /espelho - Mostra espelho de pagamento por período"""
    if not context.args or len(context.args) != 2:
        await update.message.reply_text(
            "❌ Uso incorreto!\n"
            "📊 Use: /espelho [data_inicial] [data_final]\n"
            "📅 Exemplo: /espelho 01/09/2025 07/09/2025"
        )
        return
    
    data_inicial = context.args[0]
    data_final = context.args[1]
    
    # Valida formato das datas
    try:
        datetime.strptime(data_inicial, "%d/%m/%Y")
        datetime.strptime(data_final, "%d/%m/%Y")
    except ValueError:
        await update.message.reply_text(
            "❌ Formato de data inválido!\n"
            "📅 Use DD/MM/AAAA"
        )
        return
    
    try:
        rotas = get_rotas_por_periodo(data_inicial, data_final)
        total = get_total_periodo(data_inicial, data_final)
        
        if not rotas:
            await update.message.reply_text(
                f"📅 Período: {data_inicial} até {data_final}\n\n"
                "❌ Nenhuma rota encontrada neste período."
            )
            return
        
        message = f"📅 Período: {data_inicial} até {data_final}\n\n"
        
        for rota in rotas:
            ilha_texto = "Ilha" if rota['ilha'] else "Sem ilha"
            message += f"• {rota['data']} | {rota['rota']} | {rota['carro']} | {ilha_texto} | R$ {rota['valor']:.2f}\n"
        
        message += f"\n💰 Total no período: R$ {total:.2f}"
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao consultar espelho: {str(e)}")

async def hoje_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /hoje - Mostra rotas da data atual"""
    try:
        rotas = get_rotas_hoje()
        total = get_total_hoje()
        hoje = datetime.now().strftime("%d/%m/%Y")
        
        if not rotas:
            await update.message.reply_text(
                f"📅 Rotas de hoje ({hoje})\n\n"
                "❌ Nenhuma rota registrada hoje."
            )
            return
        
        message = f"📅 Rotas de hoje ({hoje})\n\n"
        
        for rota in rotas:
            ilha_texto = "Ilha" if rota['ilha'] else "Sem ilha"
            message += f"• {rota['rota']} | {rota['carro']} | {ilha_texto} | R$ {rota['valor']:.2f}\n"
        
        message += f"\n💰 Total hoje: R$ {total:.2f}"
        
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao consultar rotas de hoje: {str(e)}")

async def todas_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /todas - Lista todas as rotas cadastradas"""
    try:
        rotas = get_todas_rotas()
        
        if not rotas:
            await update.message.reply_text(
                "📋 Todas as Rotas\n\n"
                "❌ Nenhuma rota cadastrada."
            )
            return
        
        message = "📋 Todas as Rotas\n\n"
        
        for rota in rotas:
            ilha_texto = "Ilha" if rota['ilha'] else "Sem ilha"
            message += f"• {rota['data']} | {rota['rota']} | {rota['carro']} | {ilha_texto} | R$ {rota['valor']:.2f} (ID: {rota['id']})\n"
        
        # Se a mensagem for muito longa, divide em partes
        if len(message) > 4000:
            # Divide em chunks de 4000 caracteres
            chunks = [message[i:i+4000] for i in range(0, len(message), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao listar rotas: {str(e)}")

async def deletar_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /deletar - Remove rota por ID"""
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(
            "❌ Uso incorreto!\n"
            "🗑️ Use: /deletar [id]\n"
            "📝 Exemplo: /deletar 5"
        )
        return
    
    try:
        rota_id = int(context.args[0])
        
        if delete_rota(rota_id):
            await update.message.reply_text(
                f"✅ Rota ID {rota_id} removida com sucesso!"
            )
        else:
            await update.message.reply_text(
                f"❌ Rota ID {rota_id} não encontrada!"
            )
            
    except ValueError:
        await update.message.reply_text(
            "❌ ID inválido! Digite um número inteiro."
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao deletar rota: {str(e)}")