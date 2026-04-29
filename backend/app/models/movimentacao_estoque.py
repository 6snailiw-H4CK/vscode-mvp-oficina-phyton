"""Modelo - Movimentação de Estoque"""
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from datetime import datetime
import enum


class TipoMovimentacao(str, enum.Enum):
    """Tipos de movimentação de estoque"""
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"


class MovimentacaoEstoque(Base):
    """Tabela de movimentações de estoque"""
    __tablename__ = "movimentacoes_estoque"
    
    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    tipo = Column(Enum(TipoMovimentacao), nullable=False)
    quantidade = Column(Integer, nullable=False)
    motivo = Column(String(100), nullable=True)
    observacao = Column(String(500), nullable=True)
    data_movimento = Column(DateTime, default=datetime.utcnow)
    usuario_id = Column(Integer, nullable=True)
