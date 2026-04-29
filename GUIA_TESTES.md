# 📚 SISTEMA SIMPLES - Guia Completo de Testes

**Data de Criação**: 29 de Abril de 2026  
**Versão**: 1.0.0 MVP  
**Status**: ✅ Pronto para Testes

---

## 🎯 O QUE FOI CRIADO

Um **sistema de gestão empresarial simplificado** totalmente novo e independente, com foco em:
- ✅ Cadastro de Clientes
- ✅ Cadastro de Fornecedores  
- ✅ Gestão de Produtos
- ✅ Controle de Estoque
- ✅ Ordem de Serviços

**Tecnologia Stack:**
- **Backend**: Python 3.11 + FastAPI
- **Banco de Dados**: PostgreSQL 15
- **Frontend**: HTML5 + Bootstrap 5 + JavaScript
- **Containerização**: Docker + Docker Compose

---

## 📂 LOCALIZAÇÃO

```
NOOTECH Original:    c:\NOOTECH PDV\          ← NÃO FOI ALTERADO
Sistema Novo:        c:\SistemaSimples\       ← COMPLETAMENTE NOVO
```

**Importante**: O NOOTECH PDV original está 100% intacto, nada foi modificado.

---

## 🚀 COMO ABRIR A PASTA DO NOVO SISTEMA

### Opção 1: Via Explorador de Arquivos (Recomendado)
1. **Abra uma NOVA janela do Windows Explorer** (Ctrl + Shift + Esc ou Win + E)
2. Digite na barra de endereço: `c:\SistemaSimples`
3. Pressione Enter

### Opção 2: Via PowerShell
```powershell
# Abrir pasta em explorador
explorer c:\SistemaSimples

# Ou navegar via terminal
cd c:\SistemaSimples
ls
```

### Opção 3: Via VS Code
1. Abra VS Code
2. File → Open Folder
3. Selecione `c:\SistemaSimples`
4. Clique "Select Folder"

---

## 📁 ESTRUTURA DA PASTA

```
c:\SistemaSimples\
│
├── 📄 README.md                  ← Documentação técnica
├── 📄 SETUP.md                   ← Guia de inicialização
├── 📄 .gitignore                 ← Padrões Git
├── 📄 .env                        ← Variáveis de ambiente
├── 📄 docker-compose.yml         ← Orquestração Docker
├── 📄 start.bat                  ← Script inicialização (Windows)
├── 📄 start.sh                   ← Script inicialização (Linux/Mac)
│
├── 📁 backend/                   ← API FastAPI
│   ├── 📁 app/
│   │   ├── 📁 models/            ← Modelos banco de dados
│   │   │   ├── __init__.py
│   │   │   ├── cliente.py
│   │   │   ├── fornecedor.py
│   │   │   ├── produto.py
│   │   │   ├── movimentacao_estoque.py
│   │   │   ├── ordem_servico.py
│   │   │   └── auditoria.py
│   │   │
│   │   ├── 📁 schemas/           ← Validação de dados
│   │   │   ├── __init__.py
│   │   │   ├── cliente.py
│   │   │   ├── fornecedor.py
│   │   │   ├── produto.py
│   │   │   ├── movimentacao_estoque.py
│   │   │   └── ordem_servico.py
│   │   │
│   │   ├── 📁 routes/            ← Endpoints da API
│   │   │   ├── __init__.py
│   │   │   ├── clientes.py       ← GET, POST, PUT, DELETE
│   │   │   ├── fornecedores.py   ← GET, POST, PUT, DELETE
│   │   │   ├── produtos.py       ← GET, POST, PUT, DELETE
│   │   │   ├── estoque.py        ← Movimentações
│   │   │   └── ordem_servico.py  ← GET, POST, PUT, DELETE
│   │   │
│   │   ├── 📁 services/          ← Lógica de negócio
│   │   │   └── __init__.py
│   │   │
│   │   ├── main.py               ← Aplicação principal
│   │   ├── config.py             ← Configurações
│   │   ├── database.py           ← Conexão com BD
│   │   └── __init__.py
│   │
│   ├── requirements.txt          ← Dependências Python
│   ├── Dockerfile                ← Build da aplicação
│   └── .env                      ← Variáveis de ambiente
│
├── 📁 frontend/                  ← Interface Web
│   ├── index.html                ← Dashboard principal
│   ├── clientes.html             ← ✅ Gerenciamento clientes
│   ├── produtos.html             ← ✅ Gerenciamento produtos
│   ├── fornecedores.html         ← 📋 Template (pronto)
│   ├── estoque.html              ← 📊 Relatório estoque
│   ├── ordens-servico.html       ← 📋 Template (pronto)
│   │
│   ├── 📁 css/
│   │   └── style.css             ← Estilos customizados
│   │
│   └── 📁 js/
│       └── api.js                ← Funções API
│
└── 📁 database/
    └── schema.sql                ← Script SQL completo
```

---

## ⚙️ O QUE ESTÁ IMPLEMENTADO

### ✅ MÓDULO CLIENTES
- Listar clientes com paginação
- Criar novo cliente
- Editar cliente
- Deletar cliente (soft delete)
- Validação de CPF/CNPJ duplicado

**Frontend**: Página completa funcional  
**Backend**: API REST completa  
**Banco**: Tabela com 9 campos

### ✅ MÓDULO PRODUTOS
- Listar produtos com filtros
- Criar novo produto
- Editar produto
- Deletar produto (soft delete)
- Validação de SKU duplicado
- Alerta de estoque baixo

**Frontend**: Página completa funcional  
**Backend**: API REST com filtros  
**Banco**: Tabela com 11 campos

### ✅ MÓDULO ESTOQUE
- Registrar entrada de produtos
- Registrar saída de produtos
- Ver histórico de movimentações
- Relatório resumido de estoque
- Validação de quantidade

**Frontend**: Página com resumo visual  
**Backend**: API completa de movimentações  
**Banco**: Tabela com histórico

### ✅ MÓDULO ORDEM DE SERVIÇO
- Listar ordens com filtros
- Criar nova ordem
- Editar ordem
- Cancelar ordem
- Geração automática de número
- Adicionar itens à ordem

**Frontend**: Template estruturado  
**Backend**: API REST completa  
**Banco**: Tabelas com suporte a itens

### ✅ MÓDULO FORNECEDORES
- Listar fornecedores
- Criar fornecedor
- Editar fornecedor
- Deletar fornecedor
- Validação de CNPJ

**Frontend**: Template estruturado  
**Backend**: API REST completa  
**Banco**: Tabela com 9 campos

---

## 🗄️ BANCO DE DADOS

### Tabelas Criadas (6 no total)

| Tabela | Descrição | Campos |
|--------|-----------|--------|
| `clientes` | Cadastro de clientes | id, nome, cpf_cnpj, email, telefone, endereco, cidade, estado, ativo, datas |
| `fornecedores` | Cadastro de fornecedores | id, nome, cnpj, contato, email, telefone, endereco, cidade, estado, ativo, datas |
| `produtos` | Catálogo de produtos | id, nome, sku, descricao, categoria, quantidade_atual, quantidade_minima, preco_custo, preco_venda, fornecedor_id, ativo, datas |
| `movimentacoes_estoque` | Histórico de entradas/saídas | id, produto_id, tipo, quantidade, motivo, observacao, data_movimento, usuario_id |
| `ordens_servico` | Ordens de serviço | id, numero, cliente_id, descricao, status, tecnico_responsavel, datas, valores, observacoes |
| `ordens_servico_itens` | Itens das ordens | id, ordem_servico_id, produto_id, descricao, quantidade, valor_unitario, subtotal |
| `auditoria` | Log de operações | id, modulo, operacao, tabela, registro_id, usuario, datas, dados_antes, dados_depois |

### Dados de Exemplo

**3 Clientes**:
- João Silva (CPF)
- Maria Santos (CPF)
- Empresa Ltda (CNPJ)

**2 Fornecedores**:
- Fornecedor ABC Ltda
- Distribuidor XYZ

**3 Produtos**:
- Produto A (Eletrônicos)
- Produto B (Vestuário)
- Produto C (Alimentos)

**2 Ordens de Serviço**:
- OS aberta
- OS em andamento

---

## 🔌 ENDPOINTS DA API

### Health Check
```
GET http://localhost:8000/health
GET http://localhost:8000/
GET http://localhost:8000/api/v1
```

### Clientes
```
GET    http://localhost:8000/api/v1/clientes
POST   http://localhost:8000/api/v1/clientes
GET    http://localhost:8000/api/v1/clientes/{id}
PUT    http://localhost:8000/api/v1/clientes/{id}
DELETE http://localhost:8000/api/v1/clientes/{id}
```

### Fornecedores
```
GET    http://localhost:8000/api/v1/fornecedores
POST   http://localhost:8000/api/v1/fornecedores
GET    http://localhost:8000/api/v1/fornecedores/{id}
PUT    http://localhost:8000/api/v1/fornecedores/{id}
DELETE http://localhost:8000/api/v1/fornecedores/{id}
```

### Produtos
```
GET    http://localhost:8000/api/v1/produtos
POST   http://localhost:8000/api/v1/produtos
GET    http://localhost:8000/api/v1/produtos/{id}
PUT    http://localhost:8000/api/v1/produtos/{id}
DELETE http://localhost:8000/api/v1/produtos/{id}
GET    http://localhost:8000/api/v1/produtos/estoque-baixo
```

### Estoque
```
POST   http://localhost:8000/api/v1/estoque/movimentar
GET    http://localhost:8000/api/v1/estoque/movimentacoes/{id}
GET    http://localhost:8000/api/v1/estoque/relatorio/resumo
```

### Ordens de Serviço
```
GET    http://localhost:8000/api/v1/ordens-servico
POST   http://localhost:8000/api/v1/ordens-servico
GET    http://localhost:8000/api/v1/ordens-servico/{id}
PUT    http://localhost:8000/api/v1/ordens-servico/{id}
DELETE http://localhost:8000/api/v1/ordens-servico/{id}
POST   http://localhost:8000/api/v1/ordens-servico/{id}/itens
GET    http://localhost:8000/api/v1/ordens-servico/{id}/itens
```

---

## 🧪 COMO TESTAR

### Passo 1: Abrir Terminal
```powershell
# Abra uma NOVA janela do PowerShell
# Navegue até a pasta
cd c:\SistemaSimples
```

### Passo 2: Iniciar a Aplicação
```powershell
# Windows
.\start.bat

# Ou manualmente:
docker-compose up -d
```

### Passo 3: Aguardar Inicialização
- PostgreSQL: 5-10 segundos
- FastAPI: 5 segundos
- **Total: ~15-20 segundos**

Você verá no terminal:
```
...
backend_1  | INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Passo 4: Verificar Status
```powershell
# Listar containers
docker-compose ps

# Ver logs
docker-compose logs

# Testar API
curl http://localhost:8000/health
```

### Passo 5: Acessar a Aplicação

**Abra no navegador:**

1. **Frontend (Interface Web)**
   - http://localhost:8000
   - Você verá o dashboard com 4 cards de resumo

2. **API Documentation (Swagger)**
   - http://localhost:8000/docs
   - Interface interativa para testar endpoints

3. **API Documentation (ReDoc)**
   - http://localhost:8000/redoc
   - Documentação em formato de livro

---

## 🧬 ESTRUTURA DO CÓDIGO

### Backend - models/cliente.py
```python
class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cpf_cnpj = Column(String(20), unique=True)
    email = Column(String(100))
    telefone = Column(String(20))
    # ... mais campos
    ativo = Column(Boolean, default=True)
```

### Backend - schemas/cliente.py
```python
class ClienteCreate(BaseModel):
    nome: str
    cpf_cnpj: Optional[str] = None
    email: Optional[str] = None
    # ... validações
```

### Backend - routes/clientes.py
```python
@router.get("", response_model=List[ClienteResponse])
def listar_clientes(skip: int = 0, limit: int = 100):
    # Retorna lista de clientes com paginação
    
@router.post("", response_model=ClienteResponse, status_code=201)
def criar_cliente(cliente: ClienteCreate):
    # Cria novo cliente com validações
```

### Frontend - clientes.html
```html
<!-- Modal para criar/editar -->
<div class="modal" id="modalNovoCliente">
    <form id="formCliente">
        <input type="text" id="nome" required>
        <input type="email" id="email">
        <!-- ... mais campos -->
    </form>
</div>

<!-- Tabela de clientes -->
<table>
    <tbody id="tabelaClientes">
        <!-- Preenchida dinamicamente por JavaScript -->
    </tbody>
</table>
```

### Frontend - js/api.js
```javascript
// Funções helper para chamar API
async function getClientes() {
    return apiGet('/clientes?skip=0&limit=100');
}

async function createCliente(data) {
    return apiPost('/clientes', data);
}

async function updateCliente(id, data) {
    return apiPut(`/clientes/${id}`, data);
}

async function deleteCliente(id) {
    return apiDelete(`/clientes/${id}`);
}
```

---

## 🧪 CENÁRIOS DE TESTE

### Teste 1: Dashboard
1. Acesse http://localhost:8000
2. Veja 4 cards com resumos (clientes, produtos, ordens abertas, estoque baixo)
3. Links para criar novos registros

**Esperado**: ✅ Dashboard carrega com dados

### Teste 2: Gerenciar Clientes
1. Clique em "Clientes" na navbar
2. Veja tabela com 3 clientes de exemplo
3. Clique "Novo Cliente"
4. Preencha: Nome, CPF, Email, Telefone
5. Clique "Salvar Cliente"

**Esperado**: ✅ Cliente criado aparece na tabela

### Teste 3: Editar Cliente
1. Na página de clientes, clique ícone de edição
2. Altere um campo (ex: email)
3. Clique "Salvar"

**Esperado**: ✅ Cliente atualizado na tabela

### Teste 4: Deletar Cliente
1. Clique ícone de lixo em um cliente
2. Confirme a exclusão
3. Cliente desaparece da tabela

**Esperado**: ✅ Cliente removido (soft delete)

### Teste 5: Gerenciar Produtos
1. Clique em "Produtos" na navbar
2. Veja 3 produtos de exemplo
3. Clique "Novo Produto"
4. Preencha: Nome, SKU, Preço Venda
5. Clique "Salvar Produto"

**Esperado**: ✅ Produto criado com estoque = 0

### Teste 6: API Documentation
1. Acesse http://localhost:8000/docs
2. Expanda "clientes" > GET /clientes
3. Clique "Try it out"
4. Clique "Execute"
5. Veja resposta JSON com lista de clientes

**Esperado**: ✅ API retorna lista com exemplos

### Teste 7: Estoque
1. Clique em "Estoque" na navbar
2. Veja resumo com totais
3. Veja dados carregados dinamicamente

**Esperado**: ✅ Relatório carrega com valores

### Teste 8: Erro de Validação
1. Na página de clientes, tente criar 2 clientes com CPF igual
2. Veja mensagem de erro

**Esperado**: ✅ API rejeita CPF duplicado com status 400

---

## 🔧 CONFIGURAÇÕES

### Variáveis de Ambiente (.env)
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sistema_simples
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sistema_simples
DEBUG=True
SECRET_KEY=sua-chave-secreta-super-segura
```

### Portas
- **Frontend/API**: http://localhost:8000
- **PostgreSQL**: localhost:5432

---

## 🐛 TROUBLESHOOTING

### Porta 8000 já está em uso
```powershell
# Encontrar processo
netstat -ano | findstr :8000

# Matar processo (se necessário)
taskkill /PID <PID> /F
```

### Porta 5432 já está em uso
```powershell
# Encontrar processo
netstat -ano | findstr :5432

# Parar containers
docker-compose down

# Limpar volumes
docker volume prune
```

### "PostgreSQL não conecta"
```powershell
# Ver logs
docker-compose logs postgres

# Reiniciar
docker-compose down
docker-compose up -d
# Aguarde 30 segundos
```

### "API retorna erro 500"
```powershell
# Ver logs da API
docker-compose logs backend

# Testar conexão
curl http://localhost:8000/health
```

---

## 📊 EXEMPLO DE FLUXO COMPLETO

```
1. CLIENTE ACESSA: http://localhost:8000
   ↓
2. CARREGA DASHBOARD com dados de exemplo
   ↓
3. CLICA EM "NOVO CLIENTE"
   ↓
4. PREENCHE FORMULÁRIO
   ↓
5. CLICA "SALVAR" (JavaScript chama apiPost)
   ↓
6. API FastAPI valida dados (Pydantic)
   ↓
7. INSERE NO POSTGRESQL
   ↓
8. RETORNA JSON para Frontend
   ↓
9. TABELA ATUALIZA dinamicamente
   ↓
10. ALERTA "Cliente criado com sucesso!"
```

---

## 🚨 O QUE NÃO ESTÁ IMPLEMENTADO (Ainda)

❌ Autenticação/Login  
❌ Permissões por usuário  
❌ Relatórios em PDF  
❌ Gráficos dashboard  
❌ Notificações email  
❌ Integração fiscal (NFe)  
❌ Processamento de pagamentos  
❌ Sincronização em tempo real  

**Estes podem ser adicionados conforme necessário.**

---

## 💾 PARAR A APLICAÇÃO

```powershell
# Parar containers (dados preservados)
docker-compose stop

# Remover containers (dados preservados)
docker-compose down

# Remover tudo (incluindo dados)
docker-compose down -v
```

---

## 📞 PRÓXIMAS ETAPAS SUGERIDAS

Após testar:

1. **Completar páginas faltando**
   - Fornecedores (template pronto)
   - Ordens de Serviço (template pronto)

2. **Adicionar funcionalidades**
   - Dashboard com gráficos
   - Relatórios em PDF
   - Notificações por email

3. **Melhorias**
   - Autenticação JWT
   - Testes automáticos
   - Deploy em produção

---

## 📋 RESUMO FINAL

| Item | Status | Detalhes |
|------|--------|----------|
| **Backend** | ✅ Completo | FastAPI com 5 módulos |
| **Frontend** | ✅ Parcial | 2 pages completas, 3 templates |
| **Banco de Dados** | ✅ Completo | 6 tabelas + dados exemplo |
| **Docker** | ✅ Pronto | Containerizado e testado |
| **Documentação** | ✅ Completa | README + SETUP + este guia |
| **Testes Manuais** | 🔄 Pendente | 8 cenários de teste |

---

## 🎉 ESTÁ TUDO PRONTO PARA TESTAR!

**Próximo passo:**

1. Abra nova janela do PowerShell
2. Navegue até `c:\SistemaSimples`
3. Execute `.\start.bat`
4. Aguarde 20 segundos
5. Abra http://localhost:8000 no navegador

**Divirta-se testando!** 🚀

---

**Dúvidas?** Consulte:
- `README.md` - Documentação técnica
- `SETUP.md` - Guia de inicialização
- API Docs: `http://localhost:8000/docs`

