import time

import allure
from data.schema.top_sales.TopSalesDB import TopSalesDB
from utils.base_meta import Singleton
import psycopg2
from psycopg2 import Error
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import Column, Integer, String
from utils.helpers.logger import gen_logger

logger = gen_logger(__name__)


class PostgreSession(metaclass=Singleton):
    def __init__(self, host, port, user, password, database, driver, dialect):
        self.host = host
        self.port = port
        self.user = user
        self.database = database
        self.password = password
        self.driver = driver
        self.dialect = dialect
        self.URL = f"{self.dialect}+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    def bd_connect(self):
        try:
            engine = create_engine(self.URL, echo=False, pool_pre_ping=True)
            self.engine = engine
        except Error as e:
            logger.error(f"Some Error: {e}")

    def fetch(self, table, **kwargs):
        """
        :param table: what table u search for
        :param kwargs: for WHERE condition {name=column_name,condition=condition for search}
        limit/offset
        :return:
        """
        try:
            with Session(self.engine) as session:
                if kwargs["name"] or kwargs['condition'] is None:
                    cursor = session.execute(
                        select(table).limit(kwargs['limit']).offset(kwargs['offset'])).scalars().all()
                else:
                    cursor = session.execute(
                        select(table).where(table.kwargs['name'] == kwargs['condition'])).scalar_one_or_none()
            return cursor
        except Error as e:
            logger.info(f"SQL Error {e}")

    def fetch_join(self, t1, t2, jcondition, **kwargs):
        """
        :param kwargs: t1=table1 for join, t2=table2 for join, jcondition=condition for join, condition=for WHERE select
        :return:
        """
        try:
            with Session(self.engine) as session:
                if kwargs['condition'] is None:
                    stmt = (select(kwargs['t1'], kwargs['t2']).join(kwargs['t2'], kwargs['jcondition']))
                else:
                    stmt = (select(kwargs['t1'], kwargs['t2']).join(kwargs['t2'], kwargs['jcondition']).where(
                        kwargs['condition']))
                cursor = session.execute(stmt).scalars().all()
            return cursor
        except Error as e:
            logger.info(f"SQL Error: {e}")

    def raw_sql(self, query):
        try:
            with Session(self.engine) as session:
                cursor = session.execute(text(query)).scalars().all()
            return cursor
        except Error as e:
            logger.error(f"SQL Error: {e}")

    def cleaner(self, query):
        stmt = text(query)
        try:
            with Session(self.engine) as session:
                session.execute(stmt)
                session.commit()
        except Error as e:
            logger.info(f"SQL Error {e}")

    def truncate_cleaner(self, tables: list):
        try:
            with Session(self.engine) as session:
                for table in tables:
                    session.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))
                session.commit()
        except Error as e:
            logger.error(f"SQL Error {e}")

    def delete_cleaner(self, tables: list):
        try:
            with Session(self.engine) as session:
                for table in tables:
                    session.execute(text(f"DELETE FROM {table}"))
                session.commit()
        except Error as e:
            logger.error(f"SQL Error {e}")

    def close_connection(self):
        try:
            with Session(self.engine) as session:
                session.close()
        except Error as e:
            logger.info(f"Some Error: {e}")
