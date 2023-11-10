from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Dogs(Base):
    __tablename__ = 'dogs'
    pk = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    kind = Column(String)


class Timestamps(Base):
    __tablename__ = 'timestamps'
    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
