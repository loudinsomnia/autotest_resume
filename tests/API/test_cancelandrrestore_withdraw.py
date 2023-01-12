import pytest
import json
from utils.test_classAPI import User, Admin
from src.API_DATA.test_data import USERTestData, SecretKey, Transactions, Merchant, Assets
from utils.helpers.asserts import APIAssert
from src.steps.teststep import TestAPISteps
import allure


class TestCancelWithdraw:
    user = User()
    login_data = USERTestData()
    secret = SecretKey()
    transaction = Transactions()
    merchants = Merchant()
    assets = Assets()
    checker = APIAssert()
    test_step = TestAPISteps()

    @pytest.mark.xdist_group("cancel_and_restore")
    @pytest.fixture()
    def otp_gen(self):
        return self.test_step.otp_gen_user()

    @pytest.mark.xdist_group("cancel_and_restore")
    @pytest.fixture()
    def login(self):
        return self.test_step.login_user()

    @pytest.mark.xdist_group("cancel_and_restore")
    @pytest.fixture()
    def createWithdraw(self, login):
        withdraw = self.test_step.create_withdraw(login, self.transaction.createWithdraw[0])
        withdraw_uid = json.loads(withdraw.text)
        return withdraw_uid["result"]["uid"]


    @pytest.mark.xdist_group("cancel_and_restore")
    @pytest.mark.dependency(name="cancel_to_restore")
    def test_cancelWithdraw(self, login, createWithdraw):
        self.transaction.cancelWithdraw[0]["wdUid"] = createWithdraw
        cancel = self.user.cancelWithdraw(login, self.transaction.cancelWithdraw[0])
        allure.attach(name="sent body", body=f"{self.transaction.cancelWithdraw[0]}")
        allure.attach(name="response body", body=f"{cancel.text}")
        self.checker.response_checker(cancel.status_code, cancel.text)

    @pytest.mark.dependency(depends=["cancel_to_restore"])
    @pytest.mark.xdist_group("cancel_and_restore")
    def test_restoreWithdraw(self, login):
        restore_stop_withdraw = self.user.repeatFailedWithdraw(login, self.transaction.cancelWithdraw[0])
        allure.attach(name="sent body", body=f"{self.transaction.cancelWithdraw[0]}")
        allure.attach(name="response body", body=f"{restore_stop_withdraw.text}")
        self.checker.response_checker(restore_stop_withdraw.status_code, restore_stop_withdraw.text)
