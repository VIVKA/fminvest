from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PortfolioModel(Base):
    __tablename__ = 'portfolios'
    id = Column(Integer(), primary_key=True)
    account_id = Column(Integer(), nullable=False)
    name = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), default='now()')
