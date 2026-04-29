"""Rotas - Fornecedores"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.fornecedor import Fornecedor
from app.schemas.fornecedor import FornecedorCreate, FornecedorUpdate, FornecedorResponse

router = APIRouter(prefix="/fornecedores", tags=["Fornecedores"])


@router.get("", response_model=List[FornecedorResponse])
def listar_fornecedores(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    ativo: bool = None,
    db: Session = Depends(get_db)
):
    """Lista todos os fornecedores com paginação"""
    query = db.query(Fornecedor)
    
    if ativo is not None:
        query = query.filter(Fornecedor.ativo == ativo)
    
    return query.offset(skip).limit(limit).all()


@router.get("/{fornecedor_id}", response_model=FornecedorResponse)
def obter_fornecedor(fornecedor_id: int, db: Session = Depends(get_db)):
    """Obtém um fornecedor específico"""
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return fornecedor


@router.post("", response_model=FornecedorResponse, status_code=201)
def criar_fornecedor(fornecedor: FornecedorCreate, db: Session = Depends(get_db)):
    """Cria um novo fornecedor"""
    # Verifica CNPJ duplicado
    if fornecedor.cnpj:
        db_fornecedor = db.query(Fornecedor).filter(Fornecedor.cnpj == fornecedor.cnpj).first()
        if db_fornecedor:
            raise HTTPException(status_code=400, detail="CNPJ já cadastrado")
    
    db_fornecedor = Fornecedor(**fornecedor.model_dump())
    db.add(db_fornecedor)
    db.commit()
    db.refresh(db_fornecedor)
    return db_fornecedor


@router.put("/{fornecedor_id}", response_model=FornecedorResponse)
def atualizar_fornecedor(
    fornecedor_id: int,
    fornecedor_update: FornecedorUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um fornecedor existente"""
    db_fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not db_fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    
    update_data = fornecedor_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_fornecedor, field, value)
    
    db.commit()
    db.refresh(db_fornecedor)
    return db_fornecedor


@router.delete("/{fornecedor_id}", status_code=204)
def deletar_fornecedor(fornecedor_id: int, db: Session = Depends(get_db)):
    """Deleta (desativa) um fornecedor"""
    db_fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not db_fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    
    db_fornecedor.ativo = False
    db.commit()
