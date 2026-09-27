import configparser
import framework
from urllib.parse import quote
config = configparser.ConfigParser()
config.read("config.ini")
url = config.get('auth', 'auth_url')


class Auth:
    pass
