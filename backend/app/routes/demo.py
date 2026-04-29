"""Rotas de demonstração - sem dependência de banco de dados"""
from fastapi import APIRouter, status

router = APIRouter(tags=["Demo"])

# Dados em memória para demonstração
CLIENTES_DEMO = [
    {
        "id": 1,
        "nome": "João Silva",
        "cpf_cnpj": "123.456.789-00",
        "email": "joao@email.com",
        "telefone": "11-99999-1001",
        "cidade": "São Paulo",
        "estado": "SP",
        "ativo": True
    },
    {
        "id": 2,
        "nome": "Maria Santos",
        "cpf_cnpj": "987.654.321-00",
        "email": "maria@email.com",
        "telefone": "21-99999-1002",
        "cidade": "Rio de Janeiro",
        "estado": "RJ",
        "ativo": True
    }
]

PRODUTOS_DEMO = [
    {
        "id": 1,
        "nome": "Produto A",
        "sku": "SKU-001",
        "descricao": "Descrição do Produto A",
        "categoria": "Eletrônicos",
        "quantidade_atual": 50,
        "quantidade_minima": 10,
        "preco_custo": 100.00,
        "preco_venda": 150.00,
        "fornecedor_id": 1,
        "ativo": True
    },
    {
        "id": 2,
        "nome": "Produto B",
        "sku": "SKU-002",
        "descricao": "Descrição do Produto B",
        "categoria": "Vestuário",
        "quantidade_atual": 30,
        "quantidade_minima": 5,
        "preco_custo": 50.00,
        "preco_venda": 80.00,
        "fornecedor_id": 2,
        "ativo": True
    }
]

FORNECEDORES_DEMO = [
    {
        "id": 1,
        "nome": "Fornecedor ABC Ltda",
        "cnpj": "12.345.678/0001-90",
        "email": "contato@fornecedorabc.com",
        "telefone": "11-99999-0001",
        "cidade": "São Paulo",
        "estado": "SP",
        "ativo": True
    },
    {
        "id": 2,
        "nome": "Distribuidor XYZ",
        "cnpj": "98.765.432/0001-10",
        "email": "vendas@distribuidorxyz.com",
        "telefone": "21-99999-0002",
        "cidade": "Rio de Janeiro",
        "estado": "RJ",
        "ativo": True
    }
]


@router.get("/clientes-demo", status_code=status.HTTP_200_OK)
async def listar_clientes_demo():
    """Listar clientes de demonstração (sem banco de dados)"""
    return CLIENTES_DEMO


@router.get("/produtos-demo", status_code=status.HTTP_200_OK)
async def listar_produtos_demo():
    """Listar produtos de demonstração (sem banco de dados)"""
    return PRODUTOS_DEMO


@router.get("/fornecedores-demo", status_code=status.HTTP_200_OK)
async def listar_fornecedores_demo():
    """Listar fornecedores de demonstração (sem banco de dados)"""
    return FORNECEDORES_DEMO
