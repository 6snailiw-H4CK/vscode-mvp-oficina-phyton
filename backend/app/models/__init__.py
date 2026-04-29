"""Modelos SQLAlchemy - Base"""
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime


class BaseModel(Base):
    """Classe base para todos os modelos"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ativo = Column(Boolean, default=True)
