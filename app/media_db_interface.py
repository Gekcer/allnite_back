import os

from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from ..db.create_tables import EventInfo

load_dotenv()

DB_FOLDER = os.getenv('DB_FOLDER')
DB_NAME = os.getenv('DB_NAME')
DB_URL = f'sqlite:///{os.path.join(DB_FOLDER, DB_NAME)}'


class MediaDBInterface:
    def __new__(cls, media):
        if media == 'vk':
            return super().__new__(MediaDBInterfaceVK)
        if media == 'inst':
            return super().__new__(MediaDBInterfaceInst)
        if media == 'tg':
            return super().__new__(MediaDBInterfaceTG)

    def __init__(self, media):
        self.media = media
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
        pass

    def get_media_url_by_bar_name(self, bar_name, media):
        pass

    def insert_into_db_full_event_info(self, bar_row):
        media_post_url = f'{self.media}_post_url'
        with self.get_session() as session:
            event_to_add = EventInfo(bar_name=bar_row['bar_name'],
                                     media=self.media,
                                     description=bar_row['bar_post_text'],
                                     date=bar_row['bar_event_date'],
                                     post_url=bar_row['bar_post_url'])
            session.add(event_to_add)
            session.commit()
        return self

class MediaDBInterfaceVK(MediaDBInterface):
    pass

class MediaDBInterfaceInst(MediaDBInterface):
    def get_all_bar_names(self):
        table = self.get_object_from_table('BAR')
        media_column = f'{self.media}_url'
        stmt = select(table.c['name']).where(table.c[media_column] != None)
        names = []
        with self.get_session() as session:
            result = session.execute(stmt)
            results = result.fetchall()
        return [x[0] for x in results]

    def get_media_url_by_bar_name(self, bar_name):
        table = self.get_object_from_table('BAR')
        media_column = f'{self.media}_url'
        stmt = select(table.c[media_column]).where(table.c['name'] == bar_name)
        with self.get_session() as session:
            result = session.execute(stmt)
            result = result.fetchone()[0]
        return result

class MediaDBInterfaceTG(MediaDBInterface):
    pass