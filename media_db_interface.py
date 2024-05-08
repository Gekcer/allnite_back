import os

from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_FOLDER = os.getenv('DB_FOLDER')
DB_NAME = os.getenv('DB_NAME')
DB_URL = f'sqlite:///{os.path.join(DB_FOLDER, DB_NAME)}'


class MediaDBInterface:
    def __init__(self):
        self.engine = self.create_connection()
        self.Session = self.create_session()
        self.metadata = MetaData()

    def create_connection(self):
        engine = create_engine(DB_URL)
        return engine

    def create_session(self):
        session = sessionmaker(bind=self.engine)
        return session

    def get_session(self):
        return self.Session()

    def get_object_from_table(self, table_name):
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        return table

    def get_all_bar_names(self):
        table = self.get_object_from_table('BAR')
        stmt = select(table.c['name'])
        names = []
        with self.get_session() as session:
            result = session.execute(stmt)
            results = result.fetchall()
        return [x[0] for x in results]

    def get_media_url_by_bar_name(self, bar_name, media):
        if media not in ['vk', 'inst', 'tg']:
            print('media должен быть одним из: vk, inst, tg')
            return
        table = self.get_object_from_table('BAR')
        media_column = f'{media}_url'
        stmt = select(table.c[media_column]).where(table.c['name'] == bar_name)
        with self.get_session() as session:
            result = session.execute(stmt)
            result = result.fetchone()[0]
        return result
