from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

engine = create_engine("sqlite:///all_nite_db.db", echo=True)

Base = declarative_base()


class Bar(Base):
    __tablename__ = 'BAR'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    vk_url = Column(String, nullable=True)
    tg_url = Column(String, nullable=True)
    inst_url = Column(String, nullable=True)

class ActivityInfo(Base):
    __tablename__ = 'ACTIVITYINFO'

    id = Column(Integer, primary_key=True)
    bar_id = Column(Integer, ForeignKey('BAR.id'))
    media = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date = Column(Date, nullable=True)

    bar = relationship('Bar', order_by=Bar.id, back_populates='bar')


Base.metadata.create_all(engine)