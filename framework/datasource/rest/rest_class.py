import pytest
import requests
from requests.exceptions import RequestException
from utils.base_meta import Singleton
from utils.helpers.logger import gen_logger

logger = gen_logger(__name__)


class Request(metaclass=Singleton):

    def __init__(self):
        self.req = requests.Request()
        self.session = requests.Session()

    def request_gen(self,**kwargs):
        """Генерация данный запроса для подготовки запроса через сессию"""
        for key,value in kwargs.items():
            self.req.__dict__.update({key:value})


    def request(self,url,**kwargs):
        """Создание и отправка запроса
        :param url -- url+endpoin\n
        :method -- метод GET|POST|PUT|PATCH|DELETE\n
        :headers -- заголовки в запросе\n
        :body -- тело запроса\n
        :params -- параметры запроса"""
        try:
            self.req.url = url
            self.request_gen(**kwargs)
            prep = self.req.prepare()
            return self.session.send(prep,verify=False)
        except RequestException as e:
            logger.info(f"Error while procesing request {e}")
        finally:
            self.req.__dict__.update({"data":None})
            self.req.__dict__.update({"params": None})

    def __del__(self):
        self.session.close()