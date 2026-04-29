# SETUP - Sistema Simples

## 🚀 Guia Rápido de Inicialização

### Windows
```powershell
# Navegar até o diretório
cd c:\SistemaSimples

# Executar script de inicialização
.\start.bat

# Ou manualmente:
docker-compose up -d
```

### Linux/Mac
```bash
cd /caminho/para/SistemaSimples
chmod +x start.sh
./start.sh

# Ou manualmente:
docker-compose up -d
```

---

## ✅ O que foi criado

### 📦 Backend (Python FastAPI)
```
backend/
├── app/
│   ├── models/          # Modelos de banco de dados
│   │   ├── cliente.py
│   │   ├── fornecedor.py
│   │   ├── produto.py
│   │   ├── movimentacao_estoque.py
│   │   ├── ordem_servico.py
│   │   ├── auditoria.py
│   │   └── __init__.py
│   │
│   ├── schemas/         # Validação de dados (Pydantic)
│   │   ├── cliente.py
│   │   ├── fornecedor.py
│   │   ├── produto.py
│   │   ├── movimentacao_estoque.py
│   │   ├── ordem_servico.py
│   │   └── __init__.py
│   │
│   ├── routes/          # Endpoints da API
│   │   ├── clientes.py          (CRUD Completo)
│   │   ├── fornecedores.py      (CRUD Completo)
│   │   ├── produtos.py          (CRUD Completo)
│   │   ├── estoque.py           (Movimentações)
│   │   ├── ordem_servico.py     (CRUD Completo)
│   │   └── __init__.py
│   │
│   ├── services/        # Lógica de negócio
│   │   └── __init__.py
│   │
│   ├── main.py          # Aplicação FastAPI principal
│   ├── config.py        # Configurações da app
│   ├── database.py      # Conexão com PostgreSQL
│   └── __init__.py
│
├── requirements.txt     # Dependências Python
├── Dockerfile          # Container da aplicação
└── .env                # Variáveis de ambiente
```

### 🎨 Frontend (HTML5 + Bootstrap 5)
```
frontend/
├── index.html              # Dashboard principal
├── clientes.html           # ✅ Gerenciamento de clientes (Completo)
├── fornecedores.html       # 📋 Placeholder (Pronto para implementar)
├── produtos.html           # ✅ Gerenciamento de produtos (Completo)
├── estoque.html            # 📊 Relatório de estoque (Básico)
├── ordens-servico.html     # 📋 Placeholder (Pronto para implementar)
│
├── css/
│   └── style.css           # Estilos customizados
│
└── js/
    └── api.js              # Helper functions para API
```

### 🗄️ Banco de Dados (PostgreSQL)
```
database/
└── schema.sql              # DDL completo com:
                            # - 6 tabelas principais
                            # - 2 views úteis
                            # - Dados de exemplo
                            # - Índices para performance
```

### 🐳 Containerização
```
docker-compose.yml         # Orquestração de containers
backend/Dockerfile         # Build da aplicação Python
```

### 📚 Documentação
```
README.md                  # Documentação completa
SETUP.md                   # Este arquivo
.gitignore                 # Padrões para Git
start.bat                  # Script inicialização (Windows)
start.sh                   # Script inicialização (Linux/Mac)
```

---

## 📊 Endpoints da API Implementados

### ✅ CLIENTES (Completo)
- `GET    /api/v1/clientes` - Listar com paginação
- `POST   /api/v1/clientes` - Criar novo
- `GET    /api/v1/clientes/{id}` - Obter específico
- `PUT    /api/v1/clientes/{id}` - Atualizar
- `DELETE /api/v1/clientes/{id}` - Deletar (soft delete)

### ✅ FORNECEDORES (Completo)
- `GET    /api/v1/fornecedores` - Listar
- `POST   /api/v1/fornecedores` - Criar
- `GET    /api/v1/fornecedores/{id}` - Obter
- `PUT    /api/v1/fornecedores/{id}` - Atualizar
- `DELETE /api/v1/fornecedores/{id}` - Deletar

### ✅ PRODUTOS (Completo)
- `GET    /api/v1/produtos` - Listar com filtros
- `POST   /api/v1/produtos` - Criar
- `GET    /api/v1/produtos/{id}` - Obter
- `PUT    /api/v1/produtos/{id}` - Atualizar
- `DELETE /api/v1/produtos/{id}` - Deletar
- `GET    /api/v1/produtos/estoque-baixo` - Alertas de estoque

### ✅ ESTOQUE (Funcional)
- `POST   /api/v1/estoque/movimentar` - Registrar entrada/saída
- `GET    /api/v1/estoque/movimentacoes/{id}` - Histórico
- `GET    /api/v1/estoque/relatorio/resumo` - Relatório consolidado

### ✅ ORDEM DE SERVIÇO (Completo)
- `GET    /api/v1/ordens-servico` - Listar com filtros
- `POST   /api/v1/ordens-servico` - Criar
- `GET    /api/v1/ordens-servico/{id}` - Obter
- `PUT    /api/v1/ordens-servico/{id}` - Atualizar status
- `DELETE /api/v1/ordens-servico/{id}` - Cancelar
- `POST   /api/v1/ordens-servico/{id}/itens` - Adicionar item
- `GET    /api/v1/ordens-servico/{id}/itens` - Listar itens

### ✅ HEALTH CHECK
- `GET    /health` - Status da API
- `GET    /` - Informações gerais
- `GET    /api/v1` - Info dos endpoints

---

## 🔧 Primeiros Passos

### 1. Iniciar a Aplicação

**Windows:**
```bash
cd c:\SistemaSimples
start.bat
```

**Linux/Mac:**
```bash
cd /SistemaSimples
./start.sh
```

### 2. Aguardar Inicialização
- PostgreSQL: ~5-10 segundos
- FastAPI: ~5 segundos
- Total: ~15-20 segundos

### 3. Verificar Status
```bash
# Ver logs
docker-compose logs -f

# Verificar containers
docker-compose ps

# Testar API
curl http://localhost:8000/health
```

### 4. Acessar a Aplicação
- **Frontend**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

---

## 🧪 Testando a API

### Com cURL
```bash
# Listar clientes
curl http://localhost:8000/api/v1/clientes

# Criar cliente
curl -X POST http://localhost:8000/api/v1/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "cpf_cnpj": "123.456.789-00",
    "email": "joao@email.com"
  }'

# Criar produto
curl -X POST http://localhost:8000/api/v1/produtos \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Produto Teste",
    "sku": "TEST-001",
    "preco_venda": 99.99
  }'
```

### Com Swagger UI
1. Acesse http://localhost:8000/docs
2. Clique em "Try it out" em qualquer endpoint
3. Preencha os parâmetros
4. Clique "Execute"

---

## 🔑 Credenciais Padrão

### PostgreSQL
```
Host:     localhost
Port:     5432
Database: sistema_simples
User:     postgres
Password: postgres
```

### Conexão
```
postgresql://postgres:postgres@localhost:5432/sistema_simples
```

---

## 🔄 Gerenciar Aplicação

### Ver logs
```bash
# Todos os containers
docker-compose logs -f

# Apenas backend
docker-compose logs -f backend

# Apenas banco de dados
docker-compose logs -f postgres
```

### Parar aplicação
```bash
docker-compose stop
```

### Reiniciar aplicação
```bash
docker-compose restart
```

### Remover containers (mantém dados)
```bash
docker-compose down
```

### Remover tudo (incluindo dados)
```bash
docker-compose down -v
```

### Entrar no container
```bash
# Terminal do backend
docker-compose exec backend bash

# CLI do PostgreSQL
docker-compose exec postgres psql -U postgres -d sistema_simples
```

---

## 🐛 Troubleshooting

### Porta 5432 já está em uso
```bash
# Encontrar processo usando a porta
netstat -ano | findstr :5432  # Windows
lsof -i :5432                 # Mac/Linux

# Mudar porta no docker-compose.yml
# Alterar: "5432:5432" para "5433:5432"
```

### Porta 8000 já está em uso
```bash
# Encontrar processo
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Mac/Linux

# Mudar porta no docker-compose.yml
# Alterar: "8000:8000" para "8001:8000"
```

### PostgreSQL não conecta
```bash
# Verificar logs
docker-compose logs postgres

# Tentar reconectar manualmente
docker-compose down
docker-compose up -d postgres
# Aguarde 10 segundos
docker-compose up -d backend
```

### Dados de exemplo não carregaram
```bash
# Executar schema manualmente
docker-compose exec postgres psql -U postgres -d sistema_simples -f /docker-entrypoint-initdb.d/schema.sql
```

### Erro ao submeter formulário
1. Verificar console do navegador (F12)
2. Verificar logs da API: `docker-compose logs backend`
3. Confirmar que API está rodando: `curl http://localhost:8000/health`

---

## 📈 Próximos Passos

### Curto Prazo
- [ ] Completar página de fornecedores
- [ ] Completar página de ordens de serviço
- [ ] Completar movimentação de estoque
- [ ] Adicionar validações frontend

### Médio Prazo
- [ ] Implementar autenticação/autorização (JWT)
- [ ] Adicionar testes automáticos
- [ ] Implementar paginação no frontend
- [ ] Adicionar filtros avançados

### Longo Prazo
- [ ] Dashboard com gráficos (Chart.js)
- [ ] Relatórios em PDF/Excel
- [ ] Notificações por email
- [ ] API de pagamentos integrada
- [ ] App mobile (React Native)

---

## 📞 Documentação Técnica

### Estrutura de Resposta de Erro
```json
{
  "detail": "Descrição do erro"
}
```

### Estrutura de Resposta de Sucesso
```json
{
  "id": 1,
  "nome": "Valor",
  "campo": "valor",
  "data_cadastro": "2026-04-29T10:00:00",
  "ativo": true
}
```

### Paginação
```
GET /api/v1/clientes?skip=0&limit=50
```

### Headers Recomendados
```
Content-Type: application/json
Accept: application/json
```

---

## 📚 Referências Úteis

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Bootstrap 5**: https://getbootstrap.com/docs/5.0/
- **Docker**: https://docs.docker.com/

---

## ⚖️ Licença

Projeto de código aberto - Livre para uso, modificação e distribuição

---

**Última atualização**: 29 de Abril de 2026  
**Versão**: 1.0.0  
**Status**: MVP Funcional ✅
