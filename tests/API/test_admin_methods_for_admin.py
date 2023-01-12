import pytest
from utils.test_classAPI import User, Admin
from src.API_DATA.test_data import USERTestData, SecretKey, Transactions, Merchant, Assets, \
    AdminMethods
from utils.helpers.asserts import APIAssert
from src.steps.teststep import TestAPISteps
import allure


class TestAdmin:
    admin = Admin()
    admin_methods = AdminMethods()
    user = User()
    login_data = USERTestData()
    assets = Assets()
    checker = APIAssert()
    test_step = TestAPISteps()

    @pytest.fixture()
    def otp_gen(self):
        return self.test_step.otp_gen_admin()

    @pytest.fixture()
    def login(self):
        return self.test_step.login_admin()

    @allure.step("admin_methods")
    def test_admin_methods(self, login):
        getUsers = self.admin.getUsers(login)
        allure.attach(name="response body", body=f"{getUsers.text}")
        self.checker.response_checker(getUsers.status_code, getUsers.text)

    @allure.step("getUserEvents")
    def test_getUserEvents(self, login):
        event = self.admin.getUsersEvents(login)
        allure.attach(name="response body", body=f"{event.text}")
        self.checker.response_checker(event.status_code, event.text)

    @allure.step("getAdminGasWallets")
    def test_getAdminGasWallets(self, login):
        admin_wallet = self.admin.getAdminGasWallets(login)
        allure.attach(name="response body", body=f"{admin_wallet.text}")
        self.checker.response_checker(admin_wallet.status_code, admin_wallet.text)

    @allure.step("getAdminServiceWallets")
    def test_getAdminServiceWallets(self, login):
        admin_wallet = self.admin.getAdminServiceWallets(login)
        allure.attach(name="response body", body=f"{admin_wallet.text}")
        self.checker.response_checker(admin_wallet.status_code, admin_wallet.text)

    @allure.step("getTotalSumPaysAndWds")
    def test_getTotalSumPaysAndWds(self,login):
        total = self.admin.getTotalSumPaysAndWds(login)
        allure.attach(name="response body", body=f"{total.text}")
        self.checker.response_checker(total.status_code, total.text)

    @allure.step("getServiceStat")
    def test_getServiceStat(self, login):
        service_stat = self.admin.getServiceStat(login)
        allure.attach(name="response body", body=f"{service_stat.text}")
        self.checker.response_checker(service_stat.status_code, service_stat.text)