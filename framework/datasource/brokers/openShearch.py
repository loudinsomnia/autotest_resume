from opensearchpy import OpenSearch
import time
from opensearchpy.exceptions import NotFoundError, RequestError
from opensearchpy.helpers.errors import OpenSearchException
from utils.base_meta import Singleton
from utils.helpers.logger import gen_logger

logger = gen_logger(__name__)


class OpenSearchAdapter(metaclass=Singleton):
    #OpenSearch подключается в __init__ файле
    def __init__(self, host, port, user, paswd):
        self.host = host
        self.port = port
        self.user = user
        self.paswd = paswd

    def connect(self):
        try:
            self._client = OpenSearch(
                hosts=[{'host': f'{self.host}', 'port': self.port}],
                http_compress=True,
                http_auth=(self.user, self.paswd),
                use_ssl=False,
                verify_certs=False,
                ssl_show_warn=False
            )
            logger.info(f"Connection Success {self._client.info()}")
        except OpenSearchException as e:
            logger.info(f"Connection Error {e}")

    def close(self):
        try:
            if self._client is not None:
                self._client.close()
        except OpenSearchException as e:
            logger.info(f"Error to close connection {e}")

    def message_parser(self, topik, query, timeout=20, interval=1):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                responce = self._client.search(index=topik, body=query)
                messages = [message["_source"] for message in responce["hits"]["hits"]]
                if messages:
                    return messages
            except (OpenSearchException, KeyError) as e:
                logger.info(f"Find object error {e}")
            except NotFoundError:
                logger.debug(f"Index {topik} not found yet, waiting...")
            except RequestError as e:
                logger.warning(f"Request error during polling: {e}")
            except Exception as e:
                logger.error(f"Unexpected error during polling: {e}")
            time.sleep(interval)
        logger.error(f"Timeout error during polling")
        return None

    def find_deleted_message(self,topik, query, timeout=20, interval=1):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                responce = self._client.search(index=topik, body=query)
                messages = [message["_source"] for message in responce["hits"]["hits"]]
                if len(messages) == 0:
                    return messages
            except (OpenSearchException, KeyError) as e:
                logger.info(f"Find object error {e}")
            except RequestError as e:
                logger.warning(f"Request error during polling: {e}")
            except Exception as e:
                logger.error(f"Unexpected error during polling: {e}")
            time.sleep(interval)
        logger.error(f"Timeout error during polling")
        raise AssertionError("Timeout error during polling")


    def delete_by_message(self, topik, query):
        try:
            responce = self._client.delete_by_query(index=topik, body=query)
            return responce
        except OpenSearchException as e:
            logger.debug(f"Delete object error {e}")
