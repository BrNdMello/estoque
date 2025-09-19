#!/bin/bash

echo "========================================"
echo " Sistema de Estoque de Medicamentos"
echo "========================================"
echo ""
echo "Iniciando servidor Django..."
echo ""
echo "Acesse o sistema em: http://localhost:8000"
echo ""
echo "Usuarios de teste:"
echo "- Admin: admin / admin123"
echo "- Operador: operador1 / operador123"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo "========================================"
echo ""

# Navegar para o diretório do script
cd "$(dirname "$0")"

# Ativar ambiente virtual
source venv/bin/activate

# Iniciar servidor Django
python manage.py runserver

