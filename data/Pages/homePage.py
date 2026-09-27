import pytest
from selenium.webdriver.common.by import By
from utils.helpers.waiters import Waiters
from .driver_init import InitDriver


wait = Waiters
class BaseHomePage(InitDriver):
    def __init__(self,driver):
        super().__init__(driver)

        self.create_merchant = '//span'
        self.new_name_merch = '//input'
        self.accept_new_merchant = '//span'
        self.driver = driver

class Base(BaseHomePage):
    pass

class Enter(BaseHomePage):
    pass




