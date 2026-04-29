"""Rotas - Clientes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.cliente import Cliente
from app.models.ordem_servico import OrdemServico
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("", response_model=List[ClienteResponse])
def listar_clientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    ativo: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Lista todos os clientes com paginação"""
    query = db.query(Cliente)
    
    if ativo is not None:
        query = query.filter(Cliente.ativo == ativo)
    
    return query.offset(skip).limit(limit).all()


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obter_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtém um cliente específico"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@router.post("", response_model=ClienteResponse, status_code=201)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Cria um novo cliente"""
    # Verifica CPF/CNPJ duplicado
    if cliente.cpf_cnpj:
        db_cliente = db.query(Cliente).filter(Cliente.cpf_cnpj == cliente.cpf_cnpj).first()
        if db_cliente:
            raise HTTPException(status_code=400, detail="CPF/CNPJ já cadastrado")
    
    db_cliente = Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


@router.put("/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(
    cliente_id: int,
    cliente_update: ClienteUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um cliente existente"""
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Atualiza apenas os campos fornecidos
    update_data = cliente_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_cliente, field, value)
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


@router.delete("/{cliente_id}", status_code=204)
def deletar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Deleta permanentemente um cliente"""
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    ordem_vinculada = db.query(OrdemServico).filter(OrdemServico.cliente_id == cliente_id).first()
    if ordem_vinculada:
        raise HTTPException(
            status_code=400,
            detail=(
                "Cliente vinculado a ordens de serviço. Para preservar histórico, "
                "não exclua o cliente diretamente. Revise as ordens antes de remover."
            )
        )

    db.delete(db_cliente)
    db.commit()
