#!/usr/bin/env python3
"""
Script para testar a função de espelho
"""

from db import get_rotas_por_periodo, get_total_periodo

def testar_espelho():
    """Testa a função de espelho"""
    print("Testando comando /espelho...")
    print("=" * 50)
    
    # Testa período de agosto
    data_inicial = "21/08/2025"
    data_final = "30/08/2025"
    
    print(f"Período: {data_inicial} até {data_final}")
    
    try:
        rotas = get_rotas_por_periodo(data_inicial, data_final)
        total = get_total_periodo(data_inicial, data_final)
        
        print(f"Rotas encontradas: {len(rotas)}")
        print(f"Total: R$ {total:.2f}")
        
        if rotas:
            print("\nRotas encontradas:")
            for rota in rotas:
                ilha_texto = "Ilha" if rota['ilha'] else "Sem ilha"
                print(f"• {rota['data']} | {rota['rota']} | {rota['carro']} | {ilha_texto} | R$ {rota['valor']:.2f}")
        else:
            print("❌ Nenhuma rota encontrada!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    testar_espelho()
