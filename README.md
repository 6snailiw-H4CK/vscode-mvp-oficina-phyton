# Sistema Simples - Gestão de Estoque e Ordem de Serviço

## 📋 Descrição

Sistema simples e modular para gestão de:
- 👥 **Clientes** - Cadastro e gerenciamento de clientes
- 🏭 **Fornecedores** - Gestão de fornecedores
- 📦 **Produtos** - Catálogo de produtos com preços e estoque
- 📊 **Estoque** - Controle de entradas e saídas
- 🛠️ **Ordem de Serviço** - Gestão de ordens de serviço
- 📝 **Auditoria** - Rastreamento de operações

## 🛠️ Stack Tecnológico

- **Backend**: Python 3.11 + FastAPI
- **Banco de Dados**: PostgreSQL 15
- **Frontend**: HTML5 + Bootstrap 5 + JavaScript
- **Containerização**: Docker + Docker Compose

## 📦 Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.11+ (se rodar sem Docker)
- PostgreSQL 15+ (se rodar sem Docker)

## 🚀 Como Rodar

### Opção 1: Com Docker (RECOMENDADO)

```bash
# Clonar/Acessar o diretório
cd c:\SistemaSimples

# Iniciar os containers
docker-compose up -d

# Aguardar ~30 segundos para PostgreSQL estar pronto

# Acessar a aplicação
# Frontend: http://localhost:8000
# API Docs: http://localhost:8000/docs
# API Redoc: http://localhost:8000/redoc
```

### Opção 2: Instalação Local

```bash
# 1. Criar virtualenv
python -m venv venv
.\venv\Scripts\activate  # Windows

# 2. Instalar dependências
cd backend
pip install -r requirements.txt

# 3. Configurar .env (se necessário)
# Ajustar DATABASE_URL para seu PostgreSQL local

# 4. Criar banco de dados
# Executar schema.sql no PostgreSQL

# 5. Rodar servidor
uvicorn app.main:app --reload --port 8000

# 6. Abrir no navegador
# http://localhost:8000
```

## 📚 Endpoints da API

### Clientes
```
GET    /api/v1/clientes              - Listar clientes
POST   /api/v1/clientes              - Criar cliente
GET    /api/v1/clientes/{id}         - Obter cliente
PUT    /api/v1/clientes/{id}         - Atualizar cliente
DELETE /api/v1/clientes/{id}         - Deletar cliente
```

### Fornecedores
```
GET    /api/v1/fornecedores          - Listar fornecedores
POST   /api/v1/fornecedores          - Criar fornecedor
GET    /api/v1/fornecedores/{id}     - Obter fornecedor
PUT    /api/v1/fornecedores/{id}     - Atualizar fornecedor
DELETE /api/v1/fornecedores/{id}     - Deletar fornecedor
```

### Produtos
```
GET    /api/v1/produtos              - Listar produtos
POST   /api/v1/produtos              - Criar produto
GET    /api/v1/produtos/{id}         - Obter produto
PUT    /api/v1/produtos/{id}         - Atualizar produto
DELETE /api/v1/produtos/{id}         - Deletar produto
GET    /api/v1/produtos/estoque-baixo - Produtos com estoque baixo
```

### Estoque
```
POST   /api/v1/estoque/movimentar    - Registrar movimentação
GET    /api/v1/estoque/movimentacoes/{id} - Histórico de movimentações
GET    /api/v1/estoque/relatorio/resumo - Relatório de estoque
```

### Ordens de Serviço
```
GET    /api/v1/ordens-servico        - Listar ordens
POST   /api/v1/ordens-servico        - Criar ordem
GET    /api/v1/ordens-servico/{id}   - Obter ordem
PUT    /api/v1/ordens-servico/{id}   - Atualizar ordem
DELETE /api/v1/ordens-servico/{id}   - Cancelar ordem
POST   /api/v1/ordens-servico/{id}/itens - Adicionar item
GET    /api/v1/ordens-servico/{id}/itens - Listar itens
```

## 📁 Estrutura do Projeto

```
SistemaSimples/
├── backend/
│   ├── app/
│   │   ├── models/          # Modelos SQLAlchemy
│   │   ├── schemas/         # Schemas Pydantic
│   │   ├── routes/          # Endpoints FastAPI
│   │   ├── services/        # Lógica de negócio
│   │   ├── main.py          # Aplicação principal
│   │   ├── config.py        # Configurações
│   │   └── database.py      # Conexão com BD
│   ├── requirements.txt     # Dependências Python
│   ├── Dockerfile           # Container da aplicação
│   └── .env                 # Variáveis de ambiente
├── frontend/
│   ├── index.html           # Dashboard
│   ├── clientes.html        # Página de clientes
│   ├── produtos.html        # Página de produtos
│   ├── estoque.html         # Página de estoque
│   ├── ordens-servico.html  # Página de OS
│   ├── css/
│   │   └── style.css        # Estilos customizados
│   └── js/
│       └── api.js           # Funções de API
├── database/
│   └── schema.sql           # Script de criação do BD
├── docker-compose.yml       # Orquestração de containers
└── README.md                # Este arquivo
```

## 🔧 Variáveis de Ambiente

Arquivo `.env`:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sistema_simples
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sistema_simples
SECRET_KEY=sua-chave-secreta-super-segura
DEBUG=True
```

## 🔐 Segurança

⚠️ **Importante para Produção:**
- Alterar `SECRET_KEY` em `.env`
- Alterar senha padrão do PostgreSQL
- Implementar autenticação/autorização
- Habilitar HTTPS
- Configurar rate limiting
- Validar todas as entradas

## 📊 Modelos de Dados

### Cliente
```json
{
  "id": 1,
  "nome": "João Silva",
  "cpf_cnpj": "123.456.789-00",
  "email": "joao@email.com",
  "telefone": "11-99999-1001",
  "endereco": "Rua X, 123",
  "cidade": "São Paulo",
  "estado": "SP",
  "ativo": true,
  "data_cadastro": "2026-01-01T10:00:00",
  "data_atualizacao": "2026-01-01T10:00:00"
}
```

### Produto
```json
{
  "id": 1,
  "nome": "Produto A",
  "sku": "SKU-001",
  "descricao": "Descrição do produto",
  "categoria": "Eletrônicos",
  "quantidade_atual": 50,
  "quantidade_minima": 10,
  "preco_custo": 100.00,
  "preco_venda": 150.00,
  "fornecedor_id": 1,
  "ativo": true
}
```

### Ordem de Serviço
```json
{
  "id": 1,
  "numero": "OS-20260101-A1B2",
  "cliente_id": 1,
  "descricao": "Manutenção do equipamento",
  "status": "ABERTA",
  "tecnico_responsavel": "Carlos Silva",
  "data_abertura": "2026-01-01T10:00:00",
  "data_prevista_conclusao": "2026-01-05T18:00:00",
  "data_conclusao": null,
  "valor_estimado": 500.00,
  "valor_final": null,
  "observacoes": "Cliente preferência segunda-feira"
}
```

## 🧪 Testes

```bash
# Rodar testes (quando implementados)
pytest backend/tests/ -v

# Com cobertura
pytest backend/tests/ --cov=app --cov-report=html
```

## 🐛 Troubleshooting

### PostgreSQL não conecta
```bash
# Verificar logs do container
docker-compose logs postgres

# Rebuild do container
docker-compose down
docker-compose up -d --build
```

### API retorna erro 500
```bash
# Verificar logs
docker-compose logs backend

# Entrar no container
docker-compose exec backend bash
```

### Dados de exemplo não carregaram
```bash
# Executar schema.sql manualmente
docker-compose exec postgres psql -U postgres -d sistema_simples -f /docker-entrypoint-initdb.d/schema.sql
```

## 📝 Roadmap

- [ ] Autenticação e autorização (JWT)
- [ ] Dashboard com gráficos
- [ ] Relatórios avançados (PDF/Excel)
- [ ] Notificações por email
- [ ] Integração fiscal (NFe básica)
- [ ] API de pagamentos (opcional)
- [ ] Mobile app (React Native)
- [ ] Sincronização em tempo real (WebSocket)

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação da API em:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📄 Licença

Projeto de código aberto - Livre para uso e modificação

## 👥 Autores

Desenvolvido como MVP para aprendizado e demonstração de conceitos

---

**Versão**: 1.0.0  
**Última atualização**: 29 de Abril de 2026
# vscode-mvp-oficina-phyton
