from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Bar(Base):
    __tablename__ = 'bar'

    id = Column(Integer, primary_key=True)
    name = Column(Integer, )
