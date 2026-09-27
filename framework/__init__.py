import configparser
from framework.datasource.redis.redis_connector import RedisWrapper
from framework.datasource.brokers.openShearch import OpenSearchAdapter
from framework.datasource.brokers.kafka_conection import KafkaProduce
from framework.datasource.database.posgresql_connector_wrapper import PosgreSqlConnectionWrapper, PostgreSession
from framework.datasource.rest.rest_class import Request
from framework.datasource.database.mongo_connector_wrapper import MongoDBWrapper
from utils.helpers.logger import gen_logger

config = configparser.ConfigParser()
config.read('config.ini')
logger = gen_logger(__name__)

def sql_alchemy_connect(db_name, **kwargs):
    db_user = kwargs.setdefault('db_user', kwargs["db_user"])
    db_password = kwargs.setdefault('db_password', kwargs["db_password"])
    db_host = kwargs.setdefault('db_host', kwargs["db_host"])
    db_port = kwargs.setdefault('db_port', kwargs['db_port'])
    database = PostgreSession(host=db_host, port=db_port, user=db_user, password=db_password, database=db_name,
                              driver='psycopg2', dialect='postgresql')
    database.bd_connect()
    logger.info(database)
    return database


def mongo_connect():
    host = config.get('config', 'mongo_host')
    user = config.get('config', 'mongo_user')
    password = config.get('config', 'mongo_password')
    db = config.get('config', 'mongo_db')
    collection = config.get('config', 'mongo_collection')
    return MongoDBWrapper(host=host, user=user, password=password, db=db, collection=collection)


def some_db():
    return sql_alchemy_connect(db_name=config.get('config', 'topsalesdb'),
                               db_user=config.get("config", "db_user"),
                               db_password=config.get("config", "db_password"),
                               db_host=config.get("config", "db_host"),
                               db_port=config.get("config", "db_port"))


def redis_sentinel_connect():
    redis_host = config.get('config', 'redis_host')
    redis_db = config.get('config', 'redis_db')
    redis_user = config.get('config', 'redis_user')
    redis_password = config.get('config', 'redis_password')
    sentinel_password = config.get("config", "sentinel_pass")
    sentinel_hosts = redis_host.split(',')
    return RedisWrapper(host=sentinel_hosts, db=redis_db, user=redis_user, password=redis_password,
                        sentinel_password=sentinel_password)


def redis_connect():
    redis_host = config.get('config', 'redis_host')
    redis_db = config.get('config', 'redis_db')
    redis_user = None
    redis_password = None
    return RedisWrapper(host=redis_host, db=redis_db, user=redis_user, password=redis_password)


def kafka_connect():
    kafka_host = config.get('config', 'kafka_host').split(',')
    kafka_user = config.get('config', 'kafka_user')
    kafka_passwd = config.get('config', 'kafka_passwd')
    client = KafkaProduce(kafka_host, kafka_user, kafka_passwd)
    return client


def open_search_connect():
    opensearch_host = config.get('config', 'open_search_host')
    opensearch_port = config.get('config', 'open_search_port')
    open_search_user = config.get('config', 'open_search_user')
    open_search_paswd = config.get('config', 'open_search_paswd')
    opclient = OpenSearchAdapter(host=opensearch_host,
                                 port=opensearch_port,
                                 user=open_search_user,
                                 paswd=open_search_paswd)
    return opclient


def rest_session(url, **kwargs):
    return Request().request(url=url, **kwargs)
