#!/usr/bin/env python3
"""
Script para verificar o conteúdo do banco de dados
"""

import sqlite3
from db import init_database

def verificar_banco():
    """Verifica o conteúdo do banco de dados"""
    init_database()
    
    conn = sqlite3.connect("rotas.db")
    cursor = conn.cursor()
    
    # Conta total de rotas
    cursor.execute("SELECT COUNT(*) FROM rotas")
    total = cursor.fetchone()[0]
    print(f"Total de rotas no banco: {total}")
    
    if total > 0:
        print("\nPrimeiras 10 rotas:")
        cursor.execute("SELECT * FROM rotas ORDER BY id LIMIT 10")
        rotas = cursor.fetchall()
        
        for rota in rotas:
            print(f"ID: {rota[0]}, Data: {rota[1]}, Rota: {rota[2]}, Carro: {rota[3]}, Ilha: {rota[4]}, Valor: {rota[5]}")
    
    # Verifica rotas de agosto
    print("\nRotas de agosto 2025:")
    cursor.execute("SELECT * FROM rotas WHERE data LIKE '%08/2025'")
    rotas_agosto = cursor.fetchall()
    
    for rota in rotas_agosto:
        print(f"ID: {rota[0]}, Data: {rota[1]}, Rota: {rota[2]}, Carro: {rota[3]}, Ilha: {rota[4]}, Valor: {rota[5]}")
    
    conn.close()

if __name__ == "__main__":
    verificar_banco()
