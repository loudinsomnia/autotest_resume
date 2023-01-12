import json
import pytest
from utils.test_classAPI import User
from src.API_DATA.test_data import Merchant
from src.steps.teststep import TestAPISteps
import allure
from utils.helpers.asserts import APIAssert


class TestDeleteMerchant:
    user = User()
    merchant = Merchant()
    test_step = TestAPISteps()
    checker = APIAssert()


    @pytest.fixture()
    def otp_gen(self):
        return self.test_step.otp_gen_user()


    @pytest.fixture()
    def login(self):
        return self.test_step.login_user()


    @pytest.fixture
    def create_merchant(self, login, otp_gen):
        self.merchant.createMerchant['otpToken'] = otp_gen
        merch = self.user.create_merchant(login, self.merchant.createMerchant)
        allure.attach(name="sent body", body=f"{self.merchant.createMerchant}")
        allure.attach(name="response body", body=f"{merch.text}")
        self.checker.check_to_muchmerchnat(merch.status_code, merch.text)
        response = json.loads(merch.text)
        return response["result"]["uid"]


    def test_delete_merchant(self, login, otp_gen, create_merchant):
        self.merchant.delet_merchant['otpToken'] = otp_gen
        self.merchant.delet_merchant['merchUid'] = create_merchant
        delete = self.user.deleteMerchant(login, self.merchant.delet_merchant)
        allure.attach(name="sent body", body=f"{self.merchant.delet_merchant}")
        allure.attach(name="response body", body=f"{delete.text}")
        self.checker.response_checker(delete.status_code, delete.text)

    @pytest.mark.parametrize("merchant",merchant.delet_merchant_fail)
    def test_delete_merchant_fail(self,login,otp_gen,merchant):
        merchant['otpToken'] = otp_gen
        delete_fail = self.user.deleteMerchant(login, merchant)
        allure.attach(name="sent body", body=f"{merchant}")
        allure.attach(name="response body", body=f"{delete_fail.text}")
        self.checker.response_checker(delete_fail.status_code, delete_fail.text)


