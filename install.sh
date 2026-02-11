#!/bin/bash

clear
echo "=========================================="
echo "  Caçador de Preços - Instalação"
echo "=========================================="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python 3 não encontrado!"
    echo ""
    echo "Instale Python primeiro:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  Mac: brew install python3"
    echo ""
    exit 1
fi

echo "[OK] Python encontrado"
python3 --version
echo ""

# Instalar dependências
echo "Instalando dependências..."
echo ""
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERRO] Falha na instalação"
    echo ""
    echo "Tente:"
    echo "  pip3 install --upgrade pip"
    echo "  pip3 install -r requirements.txt"
    echo ""
    exit 1
fi

echo ""
echo "=========================================="
echo "  INSTALAÇÃO CONCLUÍDA!"
echo "=========================================="
echo ""
echo "Para executar o app:"
echo "  ./run.sh"
echo "  ou: python3 main.py"
echo ""
echo "(Opcional) Configure Google Shopping:"
echo "  1. Execute o app"
echo "  2. Vá em Configurações"
echo "  3. Cole sua chave da SerpAPI"
echo ""
