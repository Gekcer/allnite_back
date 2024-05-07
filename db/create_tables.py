from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine("sqlite:///all_nite_db.db", echo=True)

Base = declarative_base()


class Bar(Base):
    __tablename__ = 'bar'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    vk_url = Column(Integer, nullable=True)
    tg_url = Column(Integer, nullable=True)
    inst_url = Column(Integer, nullable=True)

class ActivityInfo(Base):
    __tablename__ = 'activity_info'

    id = Column(Integer, primary_key=True)
    bar_id = Column(Integer, ForeignKey('bar.id'))
    media = Column(String, nullable=False)
    description = Column(String)
    date = Column(Date)

    bar = relationship('Bar', order_by=Bar.id, back_populates='bar')


Base.metadata.create_all(engine)