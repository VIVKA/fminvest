from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AccountModel(Base):
    __tablename__ = 'accounts'
    id = Column(Integer(), primary_key=True)
    token = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default='now()')
