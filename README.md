# Sistema de Gerenciamento de Estoque de Medicamentos para UBSs

Sistema completo para gerenciamento de estoque de medicamentos em Unidades Básicas de Saúde (UBSs), desenvolvido com Django e interface moderna usando TailwindCSS.

## 🚀 Funcionalidades

### ✅ Implementadas
- **Sistema de Autenticação**: Login/logout com níveis de acesso (Admin, Operador, Visualizador)
- **Dashboard Interativo**: Gráficos e indicadores em tempo real
- **Cadastro de Medicamentos**: Nome, princípio ativo, dosagem, categoria
- **Cadastro de UBSs**: Unidades de saúde com endereço e responsável
- **Controle de Estoque**: Entrada, saída e transferência de medicamentos
- **Sistema de Lotes**: Controle de validade e quantidade por lote
- **Relatórios**: Estoque atual, medicamentos vencendo, movimentações
- **Interface Responsiva**: Design moderno e limpo com TailwindCSS

### 🔄 Em Desenvolvimento
- Alertas automáticos por WhatsApp e e-mail
- Sistema de backup automático
- Integração com leitor de código de barras
- Relatórios avançados com exportação

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django 4.2.7**: Framework web Python
- **Django REST Framework**: API REST
- **SQLite**: Banco de dados (inicial)
- **Python 3.8+**: Linguagem de programação

### Frontend
- **HTML5 + CSS3**: Estrutura e estilos
- **JavaScript**: Interatividade
- **TailwindCSS**: Framework CSS
- **Chart.js**: Gráficos e visualizações
- **Font Awesome**: Ícones

### Dependências
- **django-cors-headers**: CORS para API
- **python-decouple**: Gerenciamento de configurações
- **celery**: Tarefas assíncronas (futuro)
- **redis**: Cache e filas (futuro)

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos para Instalação

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd estoque-medicamentos
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crie dados de exemplo**
   ```bash
   python create_sample_data.py
   ```

6. **Execute o servidor**
   ```bash
   python manage.py runserver
   ```

7. **Acesse o sistema**
   - Interface web: http://localhost:8000
   - Admin Django: http://localhost:8000/admin

## 👥 Usuários de Teste

O sistema vem com usuários pré-configurados:

- **Administrador**: `admin` / `admin123`
- **Operador**: `operador1` / `operador123`

## 🏗️ Estrutura do Projeto

```
estoque-medicamentos/
├── accounts/                 # Sistema de usuários e autenticação
├── medicamentos/            # Cadastro de medicamentos
├── ubs/                     # Unidades Básicas de Saúde
├── estoque/                 # Controle de estoque e movimentações
├── relatorios/              # Relatórios e dashboards
├── templates/               # Templates HTML
├── static/                  # Arquivos estáticos
├── media/                   # Arquivos de mídia
├── requirements.txt         # Dependências Python
└── manage.py               # Script de gerenciamento Django
```

## 📊 Modelos de Dados

### Usuários
- **User**: Usuários do sistema com níveis de acesso
- Níveis: Administrador, Operador, Visualizador

### Medicamentos
- **CategoriaMedicamento**: Categorias (antibióticos, analgésicos, etc.)
- **Medicamento**: Dados do medicamento (nome, princípio ativo, dosagem)

### UBSs
- **UBS**: Unidades de saúde com endereço e responsável

### Estoque
- **LoteMedicamento**: Lotes com validade e quantidade
- **MovimentacaoEstoque**: Histórico de entradas/saídas
- **EstoqueMinimo**: Configuração de estoque mínimo

## 🔌 API REST

O sistema oferece uma API REST completa:

### Autenticação
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/profile/` - Perfil do usuário

### Medicamentos
- `GET /api/medicamentos/` - Listar medicamentos
- `POST /api/medicamentos/` - Criar medicamento
- `GET /api/medicamentos/{id}/` - Detalhes do medicamento

### UBSs
- `GET /api/ubs/` - Listar UBSs
- `POST /api/ubs/` - Criar UBS

### Estoque
- `GET /api/estoque/atual/` - Estoque atual
- `GET /api/estoque/critico/` - Estoque crítico
- `POST /api/estoque/entrada/` - Entrada de estoque
- `POST /api/estoque/saida/` - Saída de estoque

## 🎨 Interface

### Características do Design
- **Minimalista e Limpo**: Design focado na usabilidade
- **Responsivo**: Funciona em desktop, tablet e mobile
- **Acessível**: Cores contrastantes e navegação intuitiva
- **Moderno**: Uso de TailwindCSS para estilização

### Paleta de Cores
- **Azul**: Cor principal (#3B82F6)
- **Verde**: Sucesso e confirmações (#10B981)
- **Vermelho**: Alertas e erros (#EF4444)
- **Amarelo**: Avisos (#F59E0B)
- **Cinza**: Textos e elementos neutros

## 🔧 Configuração

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
```

### Configuração de E-mail
Para envio de alertas por e-mail, configure as variáveis de ambiente relacionadas ao SMTP.

## 📈 Próximas Funcionalidades

- [ ] Alertas automáticos por WhatsApp
- [ ] Sistema de backup automático
- [ ] Integração com leitor de código de barras
- [ ] Relatórios em PDF/Excel
- [ ] Notificações push
- [ ] API para aplicativo mobile
- [ ] Migração para PostgreSQL/MySQL

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte ou dúvidas, entre em contato:
- Email: suporte@estoque-ubs.com
- Issues: [GitHub Issues](https://github.com/seu-usuario/estoque-medicamentos/issues)

---

**Desenvolvido com ❤️ para melhorar a gestão de medicamentos nas UBSs**

