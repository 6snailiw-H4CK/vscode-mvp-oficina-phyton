"""Schemas Pydantic - Cliente"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ClienteBase(BaseModel):
    """Schema base para Cliente"""
    nome: str
    cpf_cnpj: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None


class ClienteCreate(ClienteBase):
    """Schema para criação de Cliente"""
    pass


class ClienteUpdate(BaseModel):
    """Schema para atualização de Cliente"""
    nome: Optional[str] = None
    cpf_cnpj: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    ativo: Optional[bool] = None


class ClienteResponse(ClienteBase):
    """Schema para resposta de Cliente"""
    id: int
    ativo: bool
    data_cadastro: datetime
    data_atualizacao: datetime
    
    class Config:
        from_attributes = True
