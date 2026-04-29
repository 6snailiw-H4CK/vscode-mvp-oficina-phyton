"""Schemas Pydantic - Ordem de Serviço"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class StatusOSEnum(str, Enum):
    """Enum para status da OS"""
    ABERTA = "ABERTA"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    FECHADA = "FECHADA"
    CANCELADA = "CANCELADA"


class OrdemServicoItemBase(BaseModel):
    """Schema base para item de OS"""
    produto_id: Optional[int] = None
    descricao: Optional[str] = None
    quantidade: int = 1
    valor_unitario: Optional[float] = None
    subtotal: Optional[float] = None


class OrdemServicoItemCreate(OrdemServicoItemBase):
    """Schema para criação de item de OS"""
    pass


class OrdemServicoItemUpdate(BaseModel):
    """Schema para atualização de item de OS"""
    produto_id: Optional[int] = None
    descricao: Optional[str] = None
    quantidade: Optional[int] = None
    valor_unitario: Optional[float] = None
    subtotal: Optional[float] = None


class OrdemServicoItemResponse(OrdemServicoItemBase):
    """Schema para resposta de item de OS"""
    id: int
    
    class Config:
        from_attributes = True


class OrdemServicoBase(BaseModel):
    """Schema base para Ordem de Serviço"""
    cliente_id: int
    descricao: str
    tecnico_responsavel: Optional[str] = None
    data_prevista_conclusao: Optional[datetime] = None
    observacoes: Optional[str] = None


class OrdemServicoCreate(OrdemServicoBase):
    """Schema para criação de OS"""
    status: Optional[StatusOSEnum] = None
    valor_final: Optional[float] = None
    valor_pago: Optional[float] = None
    itens: Optional[List[OrdemServicoItemCreate]] = None



class OrdemServicoUpdate(BaseModel):
    """Schema para atualização de OS"""
    cliente_id: Optional[int] = None
    descricao: Optional[str] = None
    status: Optional[StatusOSEnum] = None
    tecnico_responsavel: Optional[str] = None
    data_prevista_conclusao: Optional[datetime] = None
    data_conclusao: Optional[datetime] = None
    valor_estimado: Optional[float] = None
    valor_final: Optional[float] = None
    valor_pago: Optional[float] = None
    observacoes: Optional[str] = None




class OrdemServicoResponse(OrdemServicoBase):
    """Schema para resposta de OS"""
    id: int
    numero: str
    status: StatusOSEnum
    data_abertura: datetime
    data_conclusao: Optional[datetime]
    valor_final: Optional[float]
    valor_pago: Optional[float]
    itens: Optional[List[OrdemServicoItemResponse]] = None
    data_cadastro: datetime
    data_atualizacao: datetime
    
    class Config:
        from_attributes = True

