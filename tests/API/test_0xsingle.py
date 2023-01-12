import allure
import pytest
import json
from src.steps.teststep import TestAPISteps
from src.API_DATA.test_data import Merchant, Assets
from utils.test_classAPI import User
from utils.helpers.asserts import APIAssert


class Test0xMerchant:
    asset = Assets()
    merchant = Merchant()
    test_step = TestAPISteps()
    user = User()
    checker = APIAssert()

    @pytest.fixture()
    def otp_gen(self):
        return self.test_step.otp_gen_user()

    @pytest.fixture()
    def login(self):
        return self.test_step.login_user()

    @pytest.fixture()
    def create0xMerchant(self,login,otp_gen):
        self.merchant.create0xsingleMerchant['otpToken'] = otp_gen
        merchant = self.user.create_merchant(login,self.merchant.create0xsingleMerchant)
        allure.attach(name='Request body',body=f"{self.merchant.create0xsingleMerchant}")
        allure.attach(name='Responce body',body=f"{merchant.text}")
        self.checker.response_checker(merchant.status_code,merchant.text)
        self.checker.single0xcheker(merchant.status_code,merchant.text)
        response = json.loads(merchant.text)
        return response["result"]["uid"]

    @pytest.mark.parametrize("chain",asset.change0xWallets)
    def test_change0xWallet(self,login,otp_gen,create0xMerchant,chain):
        chain['merchUid'] = create0xMerchant
        assets = self.user.change0xWallets(login,chain)
        allure.attach(name='Request body', body=f"{chain}")
        allure.attach(name='Responce body', body=f"{assets.text}")
        self.checker.response_checker(assets.status_code, assets.text)

