"""Schemas Pydantic - Fornecedor"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FornecedorBase(BaseModel):
    """Schema base para Fornecedor"""
    nome: str
    cnpj: Optional[str] = None
    contato: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None


class FornecedorCreate(FornecedorBase):
    """Schema para criação de Fornecedor"""
    pass


class FornecedorUpdate(BaseModel):
    """Schema para atualização de Fornecedor"""
    nome: Optional[str] = None
    cnpj: Optional[str] = None
    contato: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    ativo: Optional[bool] = None


class FornecedorResponse(FornecedorBase):
    """Schema para resposta de Fornecedor"""
    id: int
    ativo: bool
    data_cadastro: datetime
    data_atualizacao: datetime
    
    class Config:
        from_attributes = True
