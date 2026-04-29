"""Modelo - Produto"""
from app.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from datetime import datetime


class Produto(Base):
    """Tabela de produtos"""
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False, index=True)
    sku = Column(String(50), unique=True, nullable=True, index=True)
    descricao = Column(String(500), nullable=True)
    categoria = Column(String(50), nullable=True)
    quantidade_atual = Column(Integer, default=0)
    quantidade_minima = Column(Integer, default=0)
    preco_custo = Column(Float, nullable=True)
    preco_venda = Column(Float, nullable=False)
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"), nullable=True)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ativo = Column(Boolean, default=True)
