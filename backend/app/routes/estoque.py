"""Rotas - Estoque"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.produto import Produto
from app.models.movimentacao_estoque import MovimentacaoEstoque
from app.schemas.movimentacao_estoque import MovimentacaoEstoqueCreate, MovimentacaoEstoqueResponse

router = APIRouter(prefix="/estoque", tags=["Estoque"])


@router.post("/movimentar", response_model=MovimentacaoEstoqueResponse, status_code=201)
def registrar_movimentacao(
    movimentacao: MovimentacaoEstoqueCreate,
    db: Session = Depends(get_db)
):
    """Registra uma movimentação de estoque (entrada ou saída)"""
    # Verifica se o produto existe
    produto = db.query(Produto).filter(Produto.id == movimentacao.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Atualiza quantidade do produto
    if movimentacao.tipo == "ENTRADA":
        produto.quantidade_atual += movimentacao.quantidade
    else:  # SAIDA
        if produto.quantidade_atual < movimentacao.quantidade:
            raise HTTPException(status_code=400, detail="Quantidade insuficiente em estoque")
        produto.quantidade_atual -= movimentacao.quantidade
    
    # Registra a movimentação
    db_movimentacao = MovimentacaoEstoque(**movimentacao.model_dump())
    db.add(db_movimentacao)
    db.commit()
    db.refresh(db_movimentacao)
    
    return db_movimentacao


@router.get("/movimentacoes/{produto_id}", response_model=List[MovimentacaoEstoqueResponse])
def obter_movimentacoes_produto(
    produto_id: int,
    db: Session = Depends(get_db)
):
    """Obtém histórico de movimentações de um produto"""
    movimentacoes = db.query(MovimentacaoEstoque).filter(
        MovimentacaoEstoque.produto_id == produto_id
    ).order_by(MovimentacaoEstoque.data_movimento.desc()).all()
    
    return movimentacoes


@router.get("/relatorio/resumo")
def relatorio_estoque(db: Session = Depends(get_db)):
    """Relatório resumido do estoque"""
    produtos = db.query(Produto).filter(Produto.ativo == True).all()
    
    total_valor = 0
    produtos_baixos = 0
    
    for produto in produtos:
        total_valor += produto.quantidade_atual * (produto.preco_custo or 0)
        if produto.quantidade_atual <= produto.quantidade_minima:
            produtos_baixos += 1
    
    return {
        "total_produtos": len(produtos),
        "produtos_com_estoque_baixo": produtos_baixos,
        "valor_total_estoque": total_valor
    }
