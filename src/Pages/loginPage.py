import pytest
from selenium.webdriver.common.by import By
from .driver_init import InitDriver


class LoginPage(InitDriver):

    def __init__(self,driver):
        super().__init__(driver)

        self.username = '//input[@type="text"]'
        self.password = '//input[@type="password"]'
        self.log_in = '//span[text()="Log in"]'

    def enter_username(self,username):
        self.driver.find_element(By.XPATH,self.username).send_keys(username)

    def enter_passwd(self,password):
        self.driver.find_element(By.XPATH,self.password).send_keys(password)

    def click_login(self):
        self.driver.find_element(By.XPATH,self.log_in).click()



