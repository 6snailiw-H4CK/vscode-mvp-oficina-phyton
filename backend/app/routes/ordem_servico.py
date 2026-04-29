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
from app.models.movimentacao_estoque import MovimentacaoEstoque, TipoMovimentacao
from app.schemas.ordem_servico import (
    OrdemServicoCreate,
    OrdemServicoUpdate,
    OrdemServicoResponse,
    OrdemServicoItemCreate,
    OrdemServicoItemUpdate,
    OrdemServicoItemResponse,
    StatusOSEnum,
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
    """Atualiza uma OS existente e, se finalizada, realiza baixa de estoque.
    Regra:
    - Ao transitar de status != FECHADA para FECHADA: validar estoque, lançar saídas e recalcular valor_final.
    - Não permitir estoque negativo.
    - Operação atômica (transação).
    """
    db_os = db.query(OrdemServico).filter(OrdemServico.id == os_id).first()
    if not db_os:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")

    prev_status = db_os.status
    update_data = os_update.model_dump(exclude_unset=True)

    # Preparar novo status (se informado)
    is_finalizing = False
    if update_data.get("status") is not None:
        # Normalizar status recebido (string ou Enum do schema) para o Enum do modelo
        raw_status = update_data["status"]
        if isinstance(raw_status, str):
            novo_status = StatusOS(raw_status)
        else:
            # Pode ser um Enum do Pydantic; usar o .value se existir
            valor = getattr(raw_status, "value", raw_status)
            novo_status = StatusOS(valor)

        is_finalizing = prev_status != StatusOS.FECHADA and novo_status == StatusOS.FECHADA
        update_data["status"] = novo_status
        if is_finalizing and not update_data.get("data_conclusao"):
            update_data["data_conclusao"] = datetime.utcnow()

    # Validar cliente se cliente_id informado
    if update_data.get("cliente_id") is not None:
        novo_cliente = db.query(Cliente).filter(Cliente.id == update_data["cliente_id"]).first()
        if not novo_cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Aplicar demais campos na OS (sem commit ainda)
    for field, value in update_data.items():
        setattr(db_os, field, value)


    # Se vai finalizar, validar e dar baixa de estoque numa transação
    if is_finalizing:
        try:
            # Recarregar itens atuais
            itens = db.query(OrdemServicoItem).filter(OrdemServicoItem.ordem_servico_id == db_os.id).all()
            if not itens:
                # Permitir OS sem itens finalizar? Sim, baixa de estoque não necessária
                pass

            # Evitar baixa duplicada: verificar movimentações com observação da OS
            ja_baixou = (
                db.query(MovimentacaoEstoque.id)
                .filter(MovimentacaoEstoque.observacao.ilike(f"%OS {db_os.numero}%"))
                .first()
                is not None
            )
            if ja_baixou:
                # Já houve baixa associada a esta OS. Não baixar novamente.
                is_finalizing = False
            else:
                # Validar estoque por item de produto
                insuficientes = []
                for item in itens:
                    if item.produto_id is None:
                        continue
                    produto = db.query(Produto).filter(Produto.id == item.produto_id).with_for_update().first()
                    if not produto:
                        insuficientes.append({"produto_id": item.produto_id, "motivo": "Produto inexistente"})
                        continue
                    if (produto.quantidade_atual or 0) < item.quantidade:
                        insuficientes.append({"produto_id": item.produto_id, "disponivel": produto.quantidade_atual, "necessario": item.quantidade})
                if insuficientes:
                    raise HTTPException(status_code=400, detail={"erro": "Estoque insuficiente", "itens": insuficientes})

                # Efetivar baixas e registrar movimentações
                for item in itens:
                    if item.produto_id is None:
                        continue
                    produto = db.query(Produto).filter(Produto.id == item.produto_id).with_for_update().first()
                    produto.quantidade_atual = int((produto.quantidade_atual or 0) - item.quantidade)
                    mov = MovimentacaoEstoque(
                        produto_id=item.produto_id,
                        tipo=TipoMovimentacao.SAIDA,
                        quantidade=item.quantidade,
                        motivo="USO_OS",
                        observacao=f"OS {db_os.numero}"
                    )
                    db.add(mov)

            # Recalcular valor_final = soma de subtotais (mão de obra + peças)
            total = db.query(func.coalesce(func.sum(OrdemServicoItem.subtotal), 0.0)).filter(
                OrdemServicoItem.ordem_servico_id == db_os.id
            ).scalar() or 0.0
            db_os.valor_final = float(total)

            db.commit()
            db.refresh(db_os)
        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Falha ao finalizar OS: {e}")
    else:
        # Atualização comum: apenas garantir valor_final consistente se não informado
        try:
            if "valor_final" not in update_data:
                total = db.query(func.coalesce(func.sum(OrdemServicoItem.subtotal), 0.0)).filter(
                    OrdemServicoItem.ordem_servico_id == db_os.id
                ).scalar() or 0.0
                db_os.valor_final = float(total)
            db.commit()
            db.refresh(db_os)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Falha ao atualizar OS: {e}")

    return db_os


@router.delete("/{os_id}", status_code=204)
def deletar_ordem_servico(os_id: int, db: Session = Depends(get_db)):
    """Exclui uma OS e seus itens"""
    db_os = db.query(OrdemServico).filter(OrdemServico.id == os_id).first()
    if not db_os:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")
    db.delete(db_os)
    db.commit()


@router.put("/{os_id}/itens/{item_id}", response_model=OrdemServicoItemResponse)
def atualizar_item_os(
    os_id: int,
    item_id: int,
    item_update: OrdemServicoItemUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um item já adicionado a uma OS"""
    db_os = db.query(OrdemServico).filter(OrdemServico.id == os_id).first()
    if not db_os:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")

    item = db.query(OrdemServicoItem).filter(
        OrdemServicoItem.id == item_id,
        OrdemServicoItem.ordem_servico_id == os_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item da ordem de serviço não encontrado")

    update_data = item_update.model_dump(exclude_unset=True)
    if update_data.get("produto_id") is not None:
        produto = db.query(Produto).filter(Produto.id == update_data["produto_id"]).first()
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

    for field, value in update_data.items():
        setattr(item, field, value)

    if "subtotal" not in update_data and ("quantidade" in update_data or "valor_unitario" in update_data):
        item.subtotal = float((item.quantidade or 0) * (item.valor_unitario or 0))

    db.commit()
    db.refresh(item)

    total = db.query(func.coalesce(func.sum(OrdemServicoItem.subtotal), 0.0)).filter(
        OrdemServicoItem.ordem_servico_id == os_id
    ).scalar() or 0.0
    db_os.valor_final = float(total)
    db.commit()
    db.refresh(db_os)

    return item


@router.delete("/{os_id}/itens/{item_id}", status_code=204)
def deletar_item_os(os_id: int, item_id: int, db: Session = Depends(get_db)):
    """Remove um item de uma OS"""
    db_os = db.query(OrdemServico).filter(OrdemServico.id == os_id).first()
    if not db_os:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")

    item = db.query(OrdemServicoItem).filter(
        OrdemServicoItem.id == item_id,
        OrdemServicoItem.ordem_servico_id == os_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item da ordem de serviço não encontrado")

    db.delete(item)
    db.commit()

    total = db.query(func.coalesce(func.sum(OrdemServicoItem.subtotal), 0.0)).filter(
        OrdemServicoItem.ordem_servico_id == os_id
    ).scalar() or 0.0
    db_os.valor_final = float(total)
    db.commit()
    db.refresh(db_os)


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
