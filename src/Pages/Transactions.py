import time

from selenium.webdriver.common.by import By
from utils.helpers.waiters import Waiters
from selenium.webdriver.common.action_chains import ActionChains
from .driver_init import InitDriver




class BaseTransactionPage(InitDriver):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = Waiters(driver)
        self.transactions = '//div[text()="Transactions"]'
        self.export = '//span//div[text()="Export"]'
        self.csv = '//span//div[text()="CVC"]'


class ExportCSV(BaseTransactionPage):
    def open_transactions(self):
        self.wait.wait_clicable(By.XPATH, self.transactions, "60").click()

    def click_export(self):
        self.wait.wait_clicable(By.XPATH, self.export, "60").click()


    def download_csv(self):
        self.wait.wait_clicable(By.XPATH, self.csv, "60").click()
