from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

engine = create_engine("sqlite:///all_nite.db", echo=True)

Base = declarative_base()


class Bar(Base):
    __tablename__ = 'BAR'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    vk_url = Column(String, nullable=True)
    tg_url = Column(String, nullable=True)
    inst_url = Column(String, nullable=True)


class EventInfo(Base):
    __tablename__ = 'EVENTINFO'

    id = Column(Integer, primary_key=True)
    bar_name = Column(String, ForeignKey('BAR.name'))
    media = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date = Column(Date, nullable=True)
    post_url = Column(String, nullable=True)

    bar = relationship('Bar')


Base.metadata.create_all(engine)