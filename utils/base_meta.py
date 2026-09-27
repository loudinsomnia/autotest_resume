import base64
import configparser
import datetime
import json
import random
import string
import curlify
import requests
import urllib3
import os
from utils.helpers.logger import gen_logger

config = configparser.ConfigParser()
config.read('config.ini')

urllib3.disable_warnings()
logger = gen_logger(__name__)


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance
