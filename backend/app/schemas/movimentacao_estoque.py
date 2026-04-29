"""Schemas Pydantic - Movimentação de Estoque"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class TipoMovimentacaoEnum(str, Enum):
    """Enum para tipo de movimentação"""
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"


class MovimentacaoEstoqueBase(BaseModel):
    """Schema base para Movimentação de Estoque"""
    produto_id: int
    tipo: TipoMovimentacaoEnum
    quantidade: int
    motivo: Optional[str] = None
    observacao: Optional[str] = None


class MovimentacaoEstoqueCreate(MovimentacaoEstoqueBase):
    """Schema para criação de Movimentação"""
    pass


class MovimentacaoEstoqueResponse(MovimentacaoEstoqueBase):
    """Schema para resposta de Movimentação"""
    id: int
    data_movimento: datetime
    
    class Config:
        from_attributes = True
