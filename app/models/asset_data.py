from sqlalchemy import Column, Date, BigInteger, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AssetDataModel(Base):
    __tablename__ = 'asset_data'
    id = Column(Integer(), primary_key=True)
    asset_id = Column(Integer(), nullable=False)
    trade_date = Column(Date(), nullable=False)

    open_price = Column(Float(), nullable=False)
    high_price = Column(Float(), nullable=False)
    low_price = Column(Float(), nullable=False)
    close_price = Column(Float(), nullable=False)
    adjusted_close_price = Column(Float(), nullable=False)
    trade_volume = Column(BigInteger(), nullable=False)

    dividend_amount = Column(Float(), nullable=True)
    split_coefficient = Column(Float(), nullable=True)
    maturity_date = Column(Date(), nullable=True)
    coupon_percent = Column(Float(), nullable=True)
    coupon_value = Column(Float(), nullable=True)
    yield_amount = Column(Float(), nullable=True)
    accrued_interest = Column(Float(), nullable=True)
