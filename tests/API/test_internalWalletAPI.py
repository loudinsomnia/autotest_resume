import pytest
import pyotp
from utils.test_classAPI import User, API
from src.API_DATA.test_data import InternalWallet, USERTestData, Merchant
from utils.helpers.asserts import APIAssert
from src.steps.teststep import TestAPISteps
import allure
import json


class TestInternalWallet:
    internal = InternalWallet()
    user = User()
    checker = APIAssert()
    test_step = TestAPISteps()
    api = API()
    login_data = USERTestData()
    merchant = Merchant()

    @pytest.fixture()
    def otp_gen(self):
        return self.test_step.otp_gen_user()

    @pytest.fixture()
    def login(self):
        return self.test_step.login_user()

    @allure.step("createInternalWallet")
    @pytest.mark.xdist_group("internalwallet")
    @pytest.mark.parametrize("internal_data", internal.createInternalWallet)
    def test_createInternalWallet(self, otp_gen, login, internal_data):
        internal_data["otpToken"] = otp_gen
        create = self.user.createInternalWallet(login, internal_data)
        allure.attach(name="sent body", body=f"{internal_data}")
        allure.attach(name="response body", body=f"{create.text}")
        self.checker.response_checker(create.status_code, create.text)

    @pytest.fixture
    @pytest.mark.xdist_group("internalwallet")
    def get_Merchant(self):
        Merchants = self.api.getMerchantWallets(self.merchant.getWallets)
        APIAssert().response_checker(Merchants.status_code, Merchants.text)
        text = json.loads(Merchants.text)
        allure.attach(body=text["result"]["BTC"][-1]["uid"])
        return text["result"]["BTC"][-1]["uid"]

    @allure.step("switchInternalWallet")
    @pytest.mark.xdist_group("internalwallet")
    def test_changeInternalWallet(self,otp_gen,login,get_Merchant):
        self.internal.switchInternalWallet["otpToken"] = otp_gen
        self.internal.switchInternalWallet["uid"] = get_Merchant
        switch = self.user.patchMainInternalWallet(login,self.internal.switchInternalWallet)
        allure.attach(name="sent body", body=f"{self.internal.switchInternalWallet}")
        allure.attach(name="response body", body=f"{switch.text}")
        self.checker.response_checker(switch.status_code, switch.text)

    @allure.step("removeWallet")
    @pytest.mark.xdist_group("internalwallet")
    def test_removeInternalWallet(self, otp_gen, login, get_Merchant):
        self.internal.removeWallet["otpToken"] = otp_gen
        self.internal.removeWallet["uid"] = get_Merchant
        remove = self.user.removeWallet(login, self.internal.removeWallet)
        allure.attach(name="sent body", body=f"{self.internal.removeWallet}")
        allure.attach(name="response body", body=f"{remove.text}")
        self.checker.response_checker(remove.status_code, remove.text)

