import json
import os


class DeployConfig:

    def __init__(self):
        self.confapi1 = self._read_config_api()
        """pay_v1 API"""
        self.url_v1 = ConfigItem(self.confapi1["base_url"]["value"])
        self.headers = ConfigItem(self.confapi1["headers"]["value"])
        self.api = ConfigItem(self.confapi1["api"]["value"])
        self.user = ConfigItem(self.confapi1["user"]["value"])
        self.public = ConfigItem(self.confapi1["public"]["value"])
        self.admin_url = ConfigItem(self.confapi1["admin_url"]["value"])
        self.admin = ConfigItem(self.confapi1["admin"]["value"])
        self.nonloginendpoint = ConfigItem(self.confapi1["nonloginendpoint"]["value"])
        """pay_v1 UI"""
        self.confui = self._read_config_ui()
        self.log_pass = ConfigItem(self.confui["UI"]["value"])


    @staticmethod
    def _read_config_api():
        """
        Prepare config_api.json file for deploy.
        :return: None.
        """

        URL_DIR = os.path.dirname(os.path.abspath("config_api.json"))
        CONFIG_DEPLOY = os.path.join(*[URL_DIR, 'config', 'config_api.json'])
        with open(CONFIG_DEPLOY, encoding="utf-8") as config_file:
            config_url_endpoint = json.loads(config_file.read())
        return config_url_endpoint

    @staticmethod
    def _read_config_ui():
        DIR = os.path.dirname(os.path.abspath("log_pass.json"))
        CONFIG = os.path.join(*[DIR],"config","log_pass.json")
        with open(CONFIG,encoding="utf-8") as config_ui:
            log_pass = json.loads(config_ui.read())
        return log_pass

class ConfigItem:
    """
    Create object for work with dict.
    """

    def __init__(self, config_dict):
        for key, value in config_dict.items():
            self.__dict__[key] = value['value']
