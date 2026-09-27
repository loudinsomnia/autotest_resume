import allure
from kafka import KafkaProducer
from kafka.errors import KafkaError
from utils.base_meta import Singleton
import json
from utils.helpers.logger import gen_logger

logger = gen_logger(__name__)


class KafkaProduce(metaclass=Singleton):
    def __init__(self, host, user, passwd):
        self.host = host
        self.user = user
        self.passwd = passwd

    def connect(self):
        try:
            self._producer = KafkaProducer(
                bootstrap_servers=self.host,
                # security_protocol='SASL_PLAINTEXT',
                # sasl_mechanism='SCRAM-SHA-256',
                # ssl_check_hostname=False,
                # ssl_cafile=None,
                # sasl_plain_username=self.user,
                # sasl_plain_password=self.passwd,
                value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')
            )
        except KafkaError as e:
            logger.info(f"Connection Error {e}")

    def close(self):
        try:
            if self._producer is not None:
                self._producer.close()
        except KafkaError as e:
            logger.info(f"Close connection Error {e}")

    def send_message(self, topik, message, key=None):
        try:
            self._producer.send(topic=topik, key=key, value=message)
            self._producer.flush()
        except KafkaError as e:
            logger.info(f"Send message error {e}")
