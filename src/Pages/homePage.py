import pytest
from selenium.webdriver.common.by import By
from utils.helpers.waiters import Waiters
from .driver_init import InitDriver


wait = Waiters
class BaseHomePage(InitDriver):
    def __init__(self,driver):
        super().__init__(driver)

        self.create_merchant = '//span[text()="Create merchant"]'
        self.new_name_merch = '//input[@type="text"]'
        self.accept_new_merchant = '//span[text()="OK"]'
        self.driver = driver
        self.merch_choose = '//span[text()="123456"]'

class Merchant(BaseHomePage):
    def create_new_merchant(self):
        wait(self.driver).wait_clicable(By.XPATH,self.create_merchant,"60").click()

    def new_name_for_merchant(self,merch_name):
        wait(self.driver).wait_tobe_visible(By.XPATH,self.new_name_merch,"60").send_keys(merch_name)

    def create_merch(self):
        self.driver.find_element(By.XPATH,self.accept_new_merchant).click()

class EnterMerchant(BaseHomePage):


    def enter_merch(self):
        wait(self.driver).wait_clicable(By.XPATH,self.merch_choose,"60").click()




