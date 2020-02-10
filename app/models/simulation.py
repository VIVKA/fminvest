from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SimulationModel(Base):
    __tablename__ = 'simulations'
    id = Column(Integer(), primary_key=True)
    asset_key = Column(String(), nullable=False)
    weights = Column(String(), nullable=False)
    hull = Column(String(), nullable=False)
    n = Column(Integer(), nullable=False)
    created_at = Column(DateTime(timezone=True), default='now()')
