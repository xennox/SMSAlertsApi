from sqlalchemy import Column, Integer, String, BigInteger
from database import Base

class Malling(Base):
    __tablename__ = 'Malling'

    id = Column(BigInteger, primary_key=True, index=True)
    datetimestart = Column(String)
    datetimeend = Column(String)
    smstext = Column(String)
    tag = Column(Integer)

class Client(Base):
    __tablename__ = 'Client'

    id = Column(BigInteger, primary_key=True, index=True)
    tel = Column(BigInteger)
    tag = Column(Integer)
    note = Column(String)
    timebelt = Column(String)