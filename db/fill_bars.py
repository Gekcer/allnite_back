import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_tables import Bar

engine = create_engine("sqlite:///all_nite.db", echo=True)

with open('bars.json', 'r', encoding='utf-8') as j:
    bars_json = json.load(j)

Session = sessionmaker(bind=engine)
session = Session()

with session:
    for bar in bars_json:
        bar_to_add = Bar(name=bar.get('Заведения'),
                         vk_url=bar.get('Вконтакте'),
                         tg_url=bar.get('Телеграм'),
                         inst_url=bar.get('Инстаграм'))
        session.add(bar_to_add)
        session.commit()