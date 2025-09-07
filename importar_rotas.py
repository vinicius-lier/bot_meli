#!/usr/bin/env python3
"""
Script para importar rotas já realizadas para o banco de dados do RoteiroBot
"""

import sqlite3
from datetime import datetime
from db import init_database, insert_rota

def limpar_rotas_duplicadas():
    """Remove rotas duplicadas do banco de dados"""
    conn = sqlite3.connect("rotas.db")
    cursor = conn.cursor()
    
    # Remove duplicatas baseadas em data + rota
    cursor.execute('''
        DELETE FROM rotas 
        WHERE id NOT IN (
            SELECT MIN(id) 
            FROM rotas 
            GROUP BY data, rota
        )
    ''')
    
    duplicatas_removidas = cursor.rowcount
    conn.commit()
    conn.close()
    
    if duplicatas_removidas > 0:
        print(f"🧹 Removidas {duplicatas_removidas} rotas duplicadas")
    
    return duplicatas_removidas

def importar_rotas_existentes():
    """Importa as rotas já realizadas baseadas na planilha"""
    
    # Inicializa o banco de dados
    init_database()
    
    # Limpa rotas duplicadas primeiro
    limpar_rotas_duplicadas()
    
    # Dados das rotas baseados na planilha (Agosto + Setembro)
    rotas_dados = [
        # AGOSTO 2025
        ("21/08/2025", "G20_AM", "Fiorino", False, "ONDA DAS 7H"),
        ("22/08/2025", "P20_PM2", "Fiorino", False, "ONDA DAS 9H"),
        ("23/08/2025", "P25_PM", "Fiorino", False, "ONDA DAS 7H"),
        ("25/08/2025", "P4_PM2", "Van", True, "ONDA DAS 9H"),
        ("26/08/2025", "Q4_PM", "Van", True, "ONDA DAS 7H"),
        ("27/08/2025", "P12_PM2", "Van", True, "ONDA DAS 9H"),
        ("28/08/2025", "P7_PM", "Van", True, "REUNIÃO AS 7H"),
        ("29/08/2025", "P10_PM2", "Van", True, "ONDA DAS 9H"),
        ("30/08/2025", "P33_PM", "Van", True, "ONDA DAS 7H"),
        
        # SETEMBRO 2025
        ("01/09/2025", "G10_AM2", "Van", False, "ONDA DAS 7H"),
        ("01/09/2025", "P27-AM2", "Van", False, "ONDA DAS 7H"),
        ("02/09/2025", "I7_AM2", "Van", False, "ONDA DAS 7H"),
        ("03/09/2025", "P9_PM2", "Van", True, "ONDA DAS 9H"),
        ("04/09/2025", "P26-PM2", "Van", True, "ONDA DAS 9H"),
        ("04/09/2025", "P32_PM2", "Van", False, "ONDA DAS 7H"),
        ("05/09/2025", "G1_AM", "Van", False, "ONDA DAS 7H"),
        ("05/09/2025", "P27_PM2", "Van", False, "ONDA DAS 7H"),
        ("06/09/2025", "P18_PM", "Van", False, "ONDA DAS 7H"),
        ("08/09/2025", "G4_AM2", "Van", False, "ONDA DAS 7H"),
        ("08/09/2025", "P3_PM2", "Van", False, "ONDA DAS 7H"),
    ]
    
    print("🚛 Importando rotas já realizadas...")
    print("=" * 50)
    
    rotas_importadas = 0
    
    for data, rota, carro, ilha, obs in rotas_dados:
        try:
            # Insere a rota no banco
            rota_id = insert_rota(data, rota, carro, ilha)
            
            # Calcula o valor para exibição
            valor_base = 130 if carro.lower() == "van" else 110
            valor_final = valor_base + (10 if ilha else 0)
            
            print(f"✅ Rota {rota_id}: {data} | {rota} | {carro} | {'Ilha' if ilha else 'Sem ilha'} | R$ {valor_final:.2f}")
            print(f"   📝 Observação: {obs}")
            
            rotas_importadas += 1
            
        except Exception as e:
            print(f"❌ Erro ao importar rota {rota}: {e}")
    
    print("=" * 50)
    print(f"📊 Total de rotas importadas: {rotas_importadas}")
    
    # Mostra resumo
    if rotas_importadas > 0:
        print("\n🎉 Importação concluída com sucesso!")
        print("💡 Use o comando /todas no bot para ver todas as rotas")
        print("💡 Use o comando /espelho 21/08/2025 30/08/2025 para ver o período")
    else:
        print("\n⚠️ Nenhuma rota foi importada")

def verificar_rotas_existentes():
    """Verifica se já existem rotas no banco"""
    conn = sqlite3.connect("rotas.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM rotas")
    count = cursor.fetchone()[0]
    
    conn.close()
    
    return count

def limpar_todas_rotas():
    """Remove todas as rotas do banco de dados"""
    conn = sqlite3.connect("rotas.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM rotas")
    rotas_removidas = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    if rotas_removidas > 0:
        print(f"🗑️ Removidas {rotas_removidas} rotas existentes")
    
    return rotas_removidas

def main():
    """Função principal"""
    print("🤖 Importador de Rotas - RoteiroBot")
    print("=" * 50)
    
    # Verifica se já existem rotas
    rotas_existentes = verificar_rotas_existentes()
    
    if rotas_existentes > 0:
        print(f"⚠️ Já existem {rotas_existentes} rotas no banco de dados.")
        print("🔄 Vou limpar todas as rotas e importar as novas da planilha.")
        resposta = input("Deseja continuar? (s/n): ").lower()
        if resposta not in ['s', 'sim', 'y', 'yes']:
            print("❌ Importação cancelada.")
            return
        
        # Limpa todas as rotas existentes
        limpar_todas_rotas()
    
    # Importa as rotas
    importar_rotas_existentes()

if __name__ == "__main__":
    main()
