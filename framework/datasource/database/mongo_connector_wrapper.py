import logging
import time

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ClientBulkWriteException, CollectionInvalid
from utils.base_meta import Singleton
from utils.helpers.logger import gen_logger

loger = gen_logger(__name__)
handler = logging.StreamHandler()
loger.addHandler(handler)


class MongoDBWrapper(object):
    def __init__(self, host, db, collection, user, password):
        self.host = host
        self.db = db
        self.collection = collection
        self.user = user
        self.password = password

    def connect(self):
        try:
            self.client = MongoClient(
                f"mongodb://{self.user}:{self.password}@{self.host}/{self.db}?authSource=db")
        except ConnectionFailure as e:
            loger.error(f"Error {type(e).__name__}: {e}")
        except ClientBulkWriteException as e:
            loger.error(f"Error {type(e).__name__}: {e}")

    def get_info(self, query, projection):
        start_time = time.time()
        while time.time() - start_time < 10:
            try:
                db = self.client[f"{self.db}"]
                collection = db[f"{self.collection}"]
                data = collection.find_one(query, projection)
                if data:
                    return data
            except CollectionInvalid as e:
                loger.error(f"Error {type(e).__name__}: {e}")
            time.sleep(1)

    def delete_viewed(self, query):
        try:
            db = self.client[f"{self.db}"]
            collection = db[f"{self.collection}"]
            collection.delete_one(query)
            loger.info("Object delete successfully")
        except CollectionInvalid as e:
            loger.error(f"Error {type(e).__name__}: {e}")

    def close(self):
        if self.client:
            self.client.close()
