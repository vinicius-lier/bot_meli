import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

DATABASE_FILE = "rotas.db"

def init_database():
    """Inicializa o banco de dados e cria a tabela se não existir"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rotas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            rota TEXT NOT NULL,
            carro TEXT NOT NULL,
            ilha INTEGER NOT NULL,
            valor REAL NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_rota(data: str, rota: str, carro: str, ilha: bool) -> int:
    """
    Insere uma nova rota no banco de dados
    
    Args:
        data: Data da rota (DD/MM/AAAA)
        rota: Nome da rota (ex: P10-AM)
        carro: Tipo do carro (Van ou Fiorino)
        ilha: Se teve entrega em ilha (True/False)
    
    Returns:
        ID da rota inserida
    """
    # Calcula o valor baseado no carro e se teve ilha
    valor_base = 130 if carro.lower() == "van" else 110
    valor_final = valor_base + (10 if ilha else 0)
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO rotas (data, rota, carro, ilha, valor)
        VALUES (?, ?, ?, ?, ?)
    ''', (data, rota, carro, 1 if ilha else 0, valor_final))
    
    rota_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return rota_id

def get_rotas_por_periodo(data_inicial: str, data_final: str) -> List[Dict]:
    """
    Busca rotas por período
    
    Args:
        data_inicial: Data inicial (DD/MM/AAAA)
        data_final: Data final (DD/MM/AAAA)
    
    Returns:
        Lista de dicionários com as rotas
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Como as datas estão no formato DD/MM/YYYY no banco, fazemos comparação direta
    cursor.execute('''
        SELECT id, data, rota, carro, ilha, valor
        FROM rotas
        WHERE data >= ? AND data <= ?
        ORDER BY data, id
    ''', (data_inicial, data_final))
    
    rotas = []
    for row in cursor.fetchall():
        rotas.append({
            'id': row[0],
            'data': row[1],
            'rota': row[2],
            'carro': row[3],
            'ilha': bool(row[4]),
            'valor': row[5]
        })
    
    conn.close()
    return rotas

def get_rotas_hoje() -> List[Dict]:
    """
    Busca todas as rotas da data atual
    
    Returns:
        Lista de dicionários com as rotas de hoje
    """
    hoje = datetime.now().strftime("%d/%m/%Y")
    return get_rotas_por_periodo(hoje, hoje)

def get_todas_rotas() -> List[Dict]:
    """
    Busca todas as rotas cadastradas
    
    Returns:
        Lista de dicionários com todas as rotas
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, data, rota, carro, ilha, valor
        FROM rotas
        ORDER BY data DESC, id DESC
    ''')
    
    rotas = []
    for row in cursor.fetchall():
        rotas.append({
            'id': row[0],
            'data': row[1],
            'rota': row[2],
            'carro': row[3],
            'ilha': bool(row[4]),
            'valor': row[5]
        })
    
    conn.close()
    return rotas

def delete_rota(rota_id: int) -> bool:
    """
    Remove uma rota pelo ID
    
    Args:
        rota_id: ID da rota a ser removida
    
    Returns:
        True se a rota foi removida, False se não foi encontrada
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM rotas WHERE id = ?', (rota_id,))
    rows_affected = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    return rows_affected > 0

def get_total_periodo(data_inicial: str, data_final: str) -> float:
    """
    Calcula o total de valores em um período
    
    Args:
        data_inicial: Data inicial (DD/MM/AAAA)
        data_final: Data final (DD/MM/AAAA)
    
    Returns:
        Total dos valores no período
    """
    rotas = get_rotas_por_periodo(data_inicial, data_final)
    return sum(rota['valor'] for rota in rotas)

def get_total_hoje() -> float:
    """
    Calcula o total de valores de hoje
    
    Returns:
        Total dos valores de hoje
    """
    rotas = get_rotas_hoje()
    return sum(rota['valor'] for rota in rotas)