from sqlalchemy import Column, DateTime, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PortfolioActionModel(Base):
    __tablename__ = 'portfolio_actions'
    id = Column(Integer(), primary_key=True)
    portfolio_id = Column(Integer(), nullable=False)
    asset_id = Column(Integer(), nullable=False)
    action_type = Column(String(20), nullable=False)
    amount = Column(Integer(), nullable=False)
    price = Column(Float(), nullable=False)
    action_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default='now()')
