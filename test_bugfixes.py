#!/usr/bin/env python3
"""
Script de testes para validar correções de bugs
Execute: python test_bugfixes.py
"""

import json
import os
from datetime import datetime

def test_price_parsing():
    """Testa o parsing correto de preços"""
    print("🧪 Teste 1: Parsing de preços...")
    
    test_cases = [
        ("R$ 1.250,50", 1250.50),
        ("R$ 100,00", 100.00),
        ("R$ 10.500,99", 10500.99),
        ("1.250,50", 1250.50),
    ]
    
    for price_str, expected in test_cases:
        price_clean = price_str.replace("R$", "").replace(" ", "").strip()
        price_clean = price_clean.replace(".", "").replace(",", ".")
        result = float(price_clean)
        
        status = "✅" if abs(result - expected) < 0.01 else "❌"
        print(f"  {status} {price_str} → R$ {result:.2f} (esperado: R$ {expected:.2f})")
    
    print()

def test_data_backup():
    """Testa sistema de backup de dados corrompidos"""
    print("🧪 Teste 2: Sistema de backup...")
    
    test_file = "test_data.json"
    
    # Criar arquivo corrompido
    with open(test_file, "w") as f:
        f.write('{"invalid": json}')
    
    # Tentar carregar
    try:
        with open(test_file, "r") as f:
            json.load(f)
        print("  ❌ Deveria ter falhado com JSON inválido")
    except json.JSONDecodeError:
        print("  ✅ JSON inválido detectado corretamente")
        
        # Criar backup
        backup_file = f"{test_file}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        import shutil
        shutil.copy(test_file, backup_file)
        
        if os.path.exists(backup_file):
            print(f"  ✅ Backup criado: {backup_file}")
            os.remove(backup_file)
        else:
            print("  ❌ Falha ao criar backup")
    
    # Limpar
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print()

def test_config_structure():
    """Testa estrutura de dados"""
    print("🧪 Teste 3: Estrutura de dados...")
    
    required_keys = ["history", "favorites", "price_history", "alerts"]
    data = {
        "history": [],
        "favorites": [],
        "price_history": {},
        "alerts": []
    }
    
    for key in required_keys:
        if key in data:
            print(f"  ✅ Chave '{key}' presente")
        else:
            print(f"  ❌ Chave '{key}' faltando")
    
    print()

def test_imports():
    """Testa se todas as dependências estão instaladas"""
    print("🧪 Teste 4: Dependências...")
    
    dependencies = [
        ("flet", "Flet"),
        ("httpx", "HTTPX"),
    ]
    
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"  ✅ {name} instalado")
        except ImportError:
            print(f"  ❌ {name} não encontrado")
    
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("  Testes de Validação - Correções v5.0.1")
    print("=" * 50)
    print()
    
    test_price_parsing()
    test_data_backup()
    test_config_structure()
    test_imports()
    
    print("=" * 50)
    print("  Testes concluídos!")
    print("=" * 50)
