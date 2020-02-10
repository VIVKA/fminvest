from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CurrencyPairModel(Base):
    __tablename__ = 'currency_pairs'
    id = Column(Integer(), primary_key=True)
    currency_type = Column(String(10), nullable=False)
    symbol_from = Column(String(10), nullable=False)
    symbol_to = Column(String(10), nullable=False)
    updated_at = Column(DateTime(timezone=True), default='now()')
    created_at = Column(DateTime(timezone=True), default='now()')
