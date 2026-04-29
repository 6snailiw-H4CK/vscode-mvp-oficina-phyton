"""Modelo - Ordem de Serviço"""
from app.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


class StatusOS(str, enum.Enum):
    """Status da Ordem de Serviço"""
    ABERTA = "ABERTA"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    FECHADA = "FECHADA"
    CANCELADA = "CANCELADA"


class OrdemServico(Base):
    """Tabela de Ordens de Serviço"""
    __tablename__ = "ordens_servico"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(20), unique=True, nullable=False, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    descricao = Column(Text, nullable=False)
    status = Column(Enum(StatusOS), default=StatusOS.ABERTA)
    tecnico_responsavel = Column(String(100), nullable=True)
    data_abertura = Column(DateTime, default=datetime.utcnow)
    data_prevista_conclusao = Column(DateTime, nullable=True)
    data_conclusao = Column(DateTime, nullable=True)
    valor_estimado = Column(Float, nullable=True)
    valor_final = Column(Float, nullable=True)
    valor_pago = Column(Float, nullable=True)
    observacoes = Column(Text, nullable=True)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    itens = relationship(
        "OrdemServicoItem",
        back_populates="ordem_servico",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class OrdemServicoItem(Base):
    """Tabela de itens de Ordem de Serviço"""
    __tablename__ = "ordens_servico_itens"

    id = Column(Integer, primary_key=True, index=True)
    ordem_servico_id = Column(Integer, ForeignKey("ordens_servico.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=True)
    descricao = Column(String(255), nullable=True)
    quantidade = Column(Integer, nullable=False, default=1)
    valor_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    ordem_servico = relationship("OrdemServico", back_populates="itens")
