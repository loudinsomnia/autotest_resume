import json
import os
import pytest
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
from src.Pages.driver_init import InitDriver


class Aserts(InitDriver):
    def __init__(self, driver):
        super().__init__(driver)

    def console_checker(self):
        if self.driver == 'Chrome':
            for log in self.driver.get_log('browser'):
                assert log == [], f"{log['message']}"
        else:
            "Can`t parse console from firefox"

    def success_login(self):
        try:
            self.driver.find_element(By.XPATH, '//div[text()="Successfuly"]')
            return True
        except EC.NoSuchElementException:
            return False
        finally:
            return True

    def creat_merchant_success(self, merchant_name):
        try:
            self.driver.find_element(By.XPATH, f'//div[text()="Merchant {merchant_name} created"]')
        except EC.NoSuchElementException:
            return False
        finally:
            return True

    def success_create_recivewithdraw(self):
        try:
            self.driver.find_element(By.XPATH, '//div[text()="Successfuly"]')
        except EC.NoSuchElementException:
            return False
        finally:
            return True

    def login_checker(self):
        assert self.success_login() == True

    def merch_checker(self, merchant_name):
        assert self.creat_merchant_success(merchant_name) == True

    def create_recivewithdraw_checker(self):
        assert self.success_create_recivewithdraw() == True

    def withdraw_check_amount(self):
        try:
            self.driver.find_element(By.XPATH, '//div[text()="Invalid amount"]')
        except EC.NoSuchElementException:
            return False
        finally:
            return True

    def withdraw_amount(self):
        assert self.withdraw_check_amount() == True, f"No money for withdraw"

    def download_checker(self):
        assert os.path.isfile(r"C:\Temp\AlfaBit CoinApiReport.csv")


class APIAssert:

    def response_checker(self, status_code, text):
        assert "<!DOCTYPE html>" not in text, f"html in response"
        responce = json.loads(text)
        assert status_code == 200 and responce["success"] is True, f"Error in request {status_code},{responce['msg']}"

    def nonlogin_response_register(self, status_code, text):
        assert "<!DOCTYPE html>" not in text, f"html in response"
        responce = json.loads(text)
        assert status_code == 200 and responce["success"] is True or responce[
            'msg'] == 'Bad mail or password. Try other pls', f"Error in request {status_code},{responce['msg']}"

    def check_to_muchmerchnat(self, status_code, text):
        responce = json.loads(text)
        if responce["success"] is True:
            assert status_code == 200, f"Erorr in request {status_code},{responce['msg']}"
        else:
            assert status_code == 200 and responce[
                'msg'] == "Max number of merchants 3", f"Erorr in request {status_code},{responce['msg']}"

    def bulk_checker(self, status_code, text):
        responce = json.loads(text)
        assert status_code == 200 and responce["success"] is True, f"Status code {status_code}"
        for i in responce["result"]:
            assert i != "Invalid merchant", f"wrong with {i}"
            assert i["status"] == 'pending', f"Transaction faild is {responce['result']}"

    def single0xcheker(self, status_code, text):
        responce = json.loads(text)
        assert status_code == 200 and responce["success"] is True, f"Status code {status_code}"
        assert 'mainInternalAddresses' in responce['result'], f"request is ok but result{responce['result']}"
        assert responce['result']['mainInternalAddresses']['ETH'] == responce['result']['mainInternalAddresses']['BNB']
