# 🚀 Instruções Rápidas - Sistema de Estoque de Medicamentos

## ⚡ Iniciar o Sistema

### Opção 1: Script Automático (Recomendado)
```bash
# Windows
start_server.bat

# Linux/Mac
./start_server.sh
```

### Opção 2: Manual
```bash
# Ativar ambiente virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Iniciar servidor
python manage.py runserver
```

## 🔑 Acesso ao Sistema

**URL**: http://localhost:8000

### Usuários de Teste:
- **Administrador**: `admin` / `admin123`
- **Operador**: `operador1` / `operador123`

## 📱 Funcionalidades Disponíveis

### 🏠 Dashboard
- Visão geral do sistema
- Estatísticas em tempo real
- Gráficos interativos
- Estoque crítico

### 💊 Medicamentos
- Cadastro de medicamentos
- Categorias
- Busca e filtros
- CRUD completo

### 🏥 UBSs
- Cadastro de Unidades de Saúde
- Endereços e responsáveis
- Gestão completa

### 📦 Estoque
- **Estoque Atual**: Visualizar lotes e quantidades
- **Entrada**: Registrar entrada de medicamentos
- **Saída**: Registrar saída de medicamentos
- **Transferências**: Entre UBSs

### 📊 Relatórios
- Estoque atual por UBS
- Medicamentos vencendo
- Consumo mensal
- Movimentações
- Estoque crítico

## 🛠️ Comandos Úteis

### Criar Dados de Exemplo
```bash
python create_sample_data.py
```

### Criar Superusuário
```bash
python manage.py createsuperuser
```

### Aplicar Migrações
```bash
python manage.py migrate
```

### Acessar Admin Django
http://localhost:8000/admin/

## 🎨 Interface

- **Design**: Moderno e responsivo
- **Cores**: Azul, verde, vermelho, amarelo
- **Navegação**: Sidebar com menu lateral
- **Gráficos**: Chart.js para visualizações

## 📁 Estrutura do Projeto

```
estoque-medicamentos/
├── accounts/          # Usuários e autenticação
├── medicamentos/      # Cadastro de medicamentos
├── ubs/              # Unidades de saúde
├── estoque/          # Controle de estoque
├── relatorios/       # Relatórios
├── templates/        # Interface web
├── static/           # Arquivos estáticos
└── requirements.txt  # Dependências
```

## 🔧 Solução de Problemas

### Erro de Template
Se houver erro de template, verifique se todas as dependências estão instaladas:
```bash
pip install -r requirements.txt
```

### Banco de Dados
Se houver erro de banco, aplique as migrações:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Porta Ocupada
Se a porta 8000 estiver ocupada, use outra:
```bash
python manage.py runserver 8001
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs do terminal
2. Consulte o README.md completo
3. Verifique se todas as dependências estão instaladas

---

**🎉 Sistema pronto para uso!** Aproveite o sistema de gerenciamento de estoque de medicamentos!

