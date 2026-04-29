"""Rotas - Ordem de Serviço"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload
from typing import List
from datetime import datetime
from app.database import get_db
from app.models.ordem_servico import OrdemServico, OrdemServicoItem, StatusOS
from app.models.cliente import Cliente
from app.models.produto import Produto
from app.schemas.ordem_servico import (
    OrdemServicoCreate, 
    OrdemServicoUpdate, 
    OrdemServicoResponse,
    OrdemServicoItemCreate,
    OrdemServicoItemResponse,
    StatusOSEnum
)

router = APIRouter(prefix="/ordens-servico", tags=["Ordem de Serviço"])


def gerar_numero_os(db: Session) -> str:
    """Gera número único para OS"""
    from datetime import datetime
    from uuid import uuid4
    timestamp = datetime.utcnow().strftime("%Y%m%d")
    random_part = str(uuid4()).split('-')[0][:4].upper()
    return f"OS-{timestamp}-{random_part}"


@router.get("", response_model=List[OrdemServicoResponse])
def listar_ordens_servico(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: StatusOSEnum = None,
    cliente_id: int = None,
    data_inicio: datetime = None,
    data_fim: datetime = None,
    cliente_nome: str = None,
    cliente_telefone: str = None,
    db: Session = Depends(get_db)
):
    """Lista todas as ordens de serviço"""
    query = db.query(OrdemServico).options(selectinload(OrdemServico.itens))

    if cliente_nome or cliente_telefone:
        query = query.join(Cliente)

    if status:
        query = query.filter(OrdemServico.status == StatusOS(status))

    if cliente_id:
        query = query.filter(OrdemServico.cliente_id == cliente_id)

    if cliente_nome:
        query = query.filter(Cliente.nome.ilike(f"%{cliente_nome}%"))

    if cliente_telefone:
        query = query.filter(Cliente.telefone.ilike(f"%{cliente_telefone}%"))

    if data_inicio:
        query = query.filter(OrdemServico.data_abertura >= data_inicio)

    if data_fim:
        query = query.filter(OrdemServico.data_abertura <= data_fim)

    return query.order_by(OrdemServico.data_abertura.desc()).offset(skip).limit(limit).all()


@router.get("/{os_id}", response_model=OrdemServicoResponse)
def obter_ordem_servico(os_id: int, db: Session = Depends(get_db)):
    """Obtém uma OS específica"""
    os = (
        db.query(OrdemServico)
        .options(selectinload(OrdemServico.itens))
        .filter(OrdemServico.id == os_id)
        .first()
    )
    if not os:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")
    return os


@router.post("", response_model=OrdemServicoResponse, status_code=201)
def criar_ordem_servico(os_create: OrdemServicoCreate, db: Session = Depends(get_db)):
    """Cria uma nova ordem de serviço"""
    # Verifica se cliente existe
    cliente = db.query(Cliente).filter(Cliente.id == os_create.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Gera número único
    numero = gerar_numero_os(db)
    
    create_data = os_create.model_dump(exclude_unset=True)
    itens_data = create_data.pop("itens", None)
    if create_data.get("status") is not None:
        create_data["status"] = StatusOS(create_data["status"])

    db_os = OrdemServico(numero=numero, **create_data)
    db.add(db_os)
    db.commit()
    db.refresh(db_os)

    total = 0.0
    if itens_data:
        for item_data in itens_data:
            produto = None
            produto_id = item_data.get("produto_id")
            if produto_id is not None:
                produto = db.query(Produto).filter(Produto.id == produto_id).first()
                if not produto:
                    raise HTTPException(status_code=404, detail=f"Produto {produto_id} não encontrado")

            valor_unitario = item_data.get("valor_unitario")
            if valor_unitario is None and produto is not None:
                valor_unitario = produto.preco_venda
            if valor_unitario is None:
                raise HTTPException(status_code=422, detail="valor_unitario é obrigatório (ou informe produto_id)")

            quantidade = item_data.get("quantidade", 1)
            subtotal = item_data.get("subtotal")
            if subtotal is None:
                subtotal = float(quantidade) * float(valor_unitario)

            item = OrdemServicoItem(
                ordem_servico_id=db_os.id,
                produto_id=produto_id,
                descricao=item_data.get("descricao"),
                quantidade=quantidade,
                valor_unitario=valor_unitario,
                subtotal=subtotal,
            )
            db.add(item)
            total += subtotal

        db.commit()
        db.refresh(db_os)
        if total > 0:
            db_os.valor_final = total
            db.commit()
            db.refresh(db_os)
    return db_os


@router.put("/{os_id}", response_model=OrdemServicoResponse)
def atualizar_ordem_servico(
    os_id: int,
    os_update: OrdemServicoUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza uma OS existente"""
    db_os = db.query(OrdemServico).filter(OrdemServico.id == os_id).first()
    if not db_os:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")
    
    update_data = os_update.model_dump(exclude_unset=True)
    
    # Se está sendo fechada, registra data de conclusão
    if update_data.get("status") == StatusOSEnum.FECHADA and not update_data.get("data_conclusao"):
        update_data["data_conclusao"] = datetime.utcnow()

    if update_data.get("status") is not None:
        update_data["status"] = StatusOS(update_data["status"])
    
    for field, value in update_data.items():
        setattr(db_os, field, value)
    
    db.commit()
    db.refresh(db_os)
    return db_os


@router.delete("/{os_id}", status_code=204)
def cancelar_ordem_servico(os_id: int, db: Session = Depends(get_db)):
    """Cancela uma OS"""
    db_os = db.query(OrdemServico).filter(OrdemServico.id == os_id).first()
    if not db_os:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")
    
    db_os.status = StatusOS.CANCELADA
    db.commit()


@router.post("/{os_id}/itens", response_model=OrdemServicoItemResponse, status_code=201)
def adicionar_item_os(
    os_id: int,
    item_data: OrdemServicoItemCreate,
    db: Session = Depends(get_db)
):
    """Adiciona um item à OS"""
    db_os = db.query(OrdemServico).filter(OrdemServico.id == os_id).first()
    if not db_os:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")

    produto = None
    if item_data.produto_id is not None:
        produto = db.query(Produto).filter(Produto.id == item_data.produto_id).first()
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

    valor_unitario = item_data.valor_unitario
    if valor_unitario is None and produto is not None:
        valor_unitario = produto.preco_venda
    if valor_unitario is None:
        raise HTTPException(status_code=422, detail="valor_unitario é obrigatório (ou informe produto_id)")

    subtotal = item_data.subtotal
    if subtotal is None:
        subtotal = float(item_data.quantidade) * float(valor_unitario)

    item = OrdemServicoItem(
        ordem_servico_id=os_id,
        produto_id=item_data.produto_id,
        descricao=item_data.descricao,
        quantidade=item_data.quantidade,
        valor_unitario=valor_unitario,
        subtotal=subtotal,
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    total = db.query(func.coalesce(func.sum(OrdemServicoItem.subtotal), 0.0)).filter(
        OrdemServicoItem.ordem_servico_id == os_id
    ).scalar()
    db_os.valor_final = float(total)
    db.commit()
    db.refresh(db_os)

    return item


@router.get("/{os_id}/itens", response_model=List[OrdemServicoItemResponse])
def listar_itens_os(os_id: int, db: Session = Depends(get_db)):
    """Lista itens de uma OS"""
    os_exists = db.query(OrdemServico.id).filter(OrdemServico.id == os_id).first()
    if not os_exists:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")
    itens = db.query(OrdemServicoItem).filter(
        OrdemServicoItem.ordem_servico_id == os_id
    ).all()
    return itens
