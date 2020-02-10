from sqlalchemy import Column, DateTime, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ComponentModel(Base):
    __tablename__ = 'components'
    id = Column(Integer(), primary_key=True)
    account_id = Column(Integer(), nullable=False)
    component_type = Column(String(50), nullable=False)
    frequency = Column(String(50), nullable=False)
    rrule = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    quantity = Column(Float(), nullable=False)
    end_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default='now()')
