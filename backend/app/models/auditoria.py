"""Modelo - Auditoria"""
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime


class Auditoria(Base):
    """Tabela de auditoria - rastreamento de operações"""
    __tablename__ = "auditoria"
    
    id = Column(Integer, primary_key=True, index=True)
    modulo = Column(String(50), nullable=False, index=True)
    operacao = Column(String(50), nullable=False)
    tabela = Column(String(50), nullable=False)
    registro_id = Column(Integer, nullable=False)
    usuario = Column(String(100), nullable=True)
    descricao = Column(Text, nullable=True)
    dados_antes = Column(Text, nullable=True)
    dados_depois = Column(Text, nullable=True)
    data_operacao = Column(DateTime, default=datetime.utcnow, index=True)
