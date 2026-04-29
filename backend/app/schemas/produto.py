"""Schemas Pydantic - Produto"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProdutoBase(BaseModel):
    """Schema base para Produto"""
    nome: str
    sku: Optional[str] = None
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    quantidade_atual: int = 0
    quantidade_minima: int = 0
    preco_custo: Optional[float] = None
    preco_venda: float
    fornecedor_id: Optional[int] = None


class ProdutoCreate(ProdutoBase):
    """Schema para criação de Produto"""
    pass


class ProdutoUpdate(BaseModel):
    """Schema para atualização de Produto"""
    nome: Optional[str] = None
    sku: Optional[str] = None
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    quantidade_atual: Optional[int] = None
    quantidade_minima: Optional[int] = None
    preco_custo: Optional[float] = None
    preco_venda: Optional[float] = None
    fornecedor_id: Optional[int] = None
    ativo: Optional[bool] = None


class ProdutoResponse(ProdutoBase):
    """Schema para resposta de Produto"""
    id: int
    quantidade_atual: int
    ativo: bool
    data_cadastro: datetime
    data_atualizacao: datetime
    
    class Config:
        from_attributes = True
