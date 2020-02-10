from sqlalchemy import Column, Date, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CurrencyPairDataModel(Base):
    __tablename__ = 'currency_pair_data'
    id = Column(Integer(), primary_key=True)
    currency_pair_id = Column(Integer(), nullable=False)
    trade_date = Column(Date(), nullable=False)
    open_price = Column(Float(), nullable=False)
    high_price = Column(Float(), nullable=False)
    low_price = Column(Float(), nullable=False)
    close_price = Column(Float(), nullable=False)
