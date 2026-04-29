"""Rotas - Produtos"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.produto import Produto
from app.schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoResponse

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.get("", response_model=List[ProdutoResponse])
def listar_produtos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    ativo: bool = Query(True),
    categoria: str = None,
    db: Session = Depends(get_db)
):
    """Lista todos os produtos com filtros opcionais"""
    query = db.query(Produto)
    
    if ativo is not None:
        query = query.filter(Produto.ativo == ativo)
    
    if categoria:
        query = query.filter(Produto.categoria == categoria)
    
    return query.offset(skip).limit(limit).all()


@router.get("/estoque-baixo", response_model=List[ProdutoResponse])
def produtos_com_estoque_baixo(db: Session = Depends(get_db)):
    """Lista produtos com estoque abaixo do mínimo"""
    return db.query(Produto).filter(
        Produto.quantidade_atual <= Produto.quantidade_minima,
        Produto.ativo == True
    ).all()


@router.get("/{produto_id}", response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    """Obtém um produto específico"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@router.post("", response_model=ProdutoResponse, status_code=201)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    """Cria um novo produto"""
    # Verifica SKU duplicado
    if produto.sku:
        db_produto = db.query(Produto).filter(Produto.sku == produto.sku).first()
        if db_produto:
            raise HTTPException(status_code=400, detail="SKU já cadastrado")
    
    db_produto = Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto


@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int,
    produto_update: ProdutoUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um produto existente"""
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    update_data = produto_update.model_dump(exclude_unset=True)
    if update_data.get('sku') is not None and update_data.get('sku') != db_produto.sku:
        existing_sku = db.query(Produto).filter(Produto.sku == update_data['sku'], Produto.id != produto_id).first()
        if existing_sku:
            raise HTTPException(status_code=400, detail="SKU já cadastrado")

    for field, value in update_data.items():
        setattr(db_produto, field, value)
    
    db.commit()
    db.refresh(db_produto)
    return db_produto


@router.delete("/{produto_id}", status_code=204)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    """Desativa um produto (soft delete)"""
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db_produto.ativo = False
    db.commit()
