"""Modelo - Fornecedor"""
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime


class Fornecedor(Base):
    """Tabela de fornecedores"""
    __tablename__ = "fornecedores"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, index=True)
    cnpj = Column(String(20), unique=True, nullable=True, index=True)
    contato = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True, index=True)
    telefone = Column(String(20), nullable=True)
    endereco = Column(String(255), nullable=True)
    cidade = Column(String(50), nullable=True)
    estado = Column(String(2), nullable=True)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ativo = Column(Boolean, default=True)
