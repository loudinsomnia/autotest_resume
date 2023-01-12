import base64
import string

import allure
import pytest
import pyotp
import json
from utils.helpers.waiters import Waiters
from src.Pages.loginPage import LoginPage
from src.Pages.OTP import OTPtokken
from selenium.webdriver.common.by import By
from utils.helpers.asserts import Aserts, APIAssert
from src.Pages.homePage import EnterMerchant
from selenium.common.exceptions import TimeoutException
from utils.test_classAPI import User
from conftest import config
from src.API_DATA.test_data import USERTestData, AdminMethods


class TestSteps:
    def login(self, driver):
        try:
            driver.get(config.log_pass.url)
            login = LoginPage(driver)
            Waiters(driver).wait_until_visible(By.XPATH, '//div[@id="global-spinner"]', "60")
            login.enter_username(username=config.log_pass.login)
            login.enter_passwd(password=config.log_pass.password)
            login.click_login()
            otp = OTPtokken(driver)
            otp.enter_otp()
            otp.click_ok()
            asert = Aserts(driver)
            asert.console_checker()
        except TimeoutException:
            allure.attach(name="Time out exceprion", body="OTP validation end")

    def enter_merchant(self, driver):
        try:
            merch = EnterMerchant(driver)
            merch.enter_merch()
            asert = Aserts(driver)
            asert.console_checker()
        except TimeoutException:
            allure.attach(name="Time out exceprion", body="OTP validation end")


class TestAPISteps:
    user = User()
    checker = APIAssert()
    login_data = USERTestData()
    admin_data = AdminMethods()

    def otp_gen_user(self):
        pass

    def login_user(self):
        self.login_data.login['otpToken'] = self.otp_gen_user()
        login = self.user.login(self.login_data.login)
        allure.attach(name="response body", body=f"{login.text}")
        self.checker.response_checker(login.status_code, login.text)
        jwt = json.loads(login.text)
        return jwt["result"]

    def otp_gen_admin(self):
        pass

    def login_admin(self):
        self.admin_data.login_admin['otpToken'] = self.otp_gen_admin()
        login = self.user.login(self.admin_data.login_admin)
        allure.attach(name="response body", body=f"{login.text}")
        self.checker.response_checker(login.status_code, login.text)
        jwt = json.loads(login.text)
        return jwt["result"]

    def create_withdraw(self, login, cr_withdraw):
        withdraw = self.user.createWithdraw(login, cr_withdraw)
        allure.attach(name="sent body", body=f"{cr_withdraw}")
        allure.attach(name="response body", body=f"{withdraw.text}")
        self.checker.response_checker(withdraw.status_code, withdraw.text)
        return withdraw
