import logging
import time

import redis
from redis.sentinel import Sentinel
from utils.base_meta import Singleton
from utils.helpers.logger import gen_logger
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)


class RedisWrapper(metaclass=Singleton):
    def __init__(self, host, db, user, password, sentinel_password):
        self.host = host
        self.db = db
        self.user = user
        self.password = password
        self.sentinels = []
        self.sentinel_password = sentinel_password
        self.sentinels = []
        for item in self.host:
            h, p = item.split(':')
            self.sentinels.append((h, int(p)))
        self._sentinel_manager = self.sentinel_master()

    def redis_connect(self):
        try:
            self._client = redis.Redis(host=self.host, db=self.db, decode_responses=True)
            self._client.ping()
        except redis.ConnectionError as e:
            logging.info(f"Error {type(e).__name__}: {e}")

    def sentinel_master(self):
        return Sentinel(self.sentinels, sentinel_kwargs={'username': "default", 'password': self.sentinel_password})

    def redis_sentinel_connect(self):
        try:
            if self._sentinel_manager:
                self._client = self._sentinel_manager.master_for(service_name='redis-rdb-aof', db=self.db,
                                                                 username=self.user, password=self.password)
                self._client.ping()
                logger.info("Получен доступ к мастеру редис")
        except redis.exceptions.AuthenticationError as e:
            logger.error(f"Ошибка авторизации (Неверный юзер/пароль): {e}")
            self._client = None
            raise
        except redis.exceptions.ConnectionError as e:
            logger.error(f"Ошибка сети/подключения (Sentinel или Redis недоступны): {e}")
            self._client = None
            raise

    def get_all_hash(self, key):
        try:
            self._client.hgetall(key)
        except redis.exceptions.RedisError as e:
            logging.info(f"Error {type(e).__name__}: {e}")

    def pipeline_hash(self, chanel, hash_dict):
        try:
            pipe = self._client.pipeline()
            for key in hash_dict:
                pipe.hgetall(f"{chanel}:{key}")
                logger.info(f"{chanel}:{key}")
            all_hash = pipe.execute()
            new_dict = {}
            for key, value in zip(hash_dict, all_hash):
                new_dict[key] = value
            return new_dict
        except redis.exceptions.RedisError as e:
            logging.info(f"Error {type(e).__name__}: {e}")

    def monitor_new_hash(self, chanel, timeout):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                data = self._client.smembers(chanel)
                if data:
                    logger.info(f"find {data}")
                    return data
            except redis.exceptions.RedisError as e:
                logging.info(f"Error {type(e).__name__}: {e}")
            time.sleep(1)

    def redis_close(self):
        try:
            self._client.connection_pool.disconnect()
            logging.info(f"Redis connection close")
        except redis.exceptions.RedisError as e:
            logging.info(f"Error {type(e).__name__}: {e}")
