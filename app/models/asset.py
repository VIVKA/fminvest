from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AssetModel(Base):
    __tablename__ = 'assets'
    id = Column(Integer(), primary_key=True)
    asset_type = Column(String(50), nullable=False)
    ticker = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    country = Column(String(10), nullable=False)
    sector = Column(String(50), nullable=False)
    currency = Column(String(10), nullable=False)
    updated_at = Column(DateTime(timezone=True), default='now()')
    created_at = Column(DateTime(timezone=True), default='now()')
