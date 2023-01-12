import pytest
from utils.test_classAPI import User
from src.API_DATA.test_data import APIKey,USERTestData
from utils.helpers.asserts import APIAssert
from src.steps.teststep import TestAPISteps
import allure


class TestAPIKey:
    user = User()
    api_key = APIKey()
    checker = APIAssert()
    login_data = USERTestData()
    test_step = TestAPISteps()

    @pytest.fixture()
    def otp_gen(self):
        return self.test_step.otp_gen_user()

    @pytest.fixture()
    def login(self):
        return self.test_step.login_user()

    @pytest.mark.xdist_group("api_key")
    @pytest.mark.dependency(name="api_key")
    def test_createApiKey(self, login, otp_gen):
        self.api_key.createApiKey[0]['otpToken'] = otp_gen
        cr_api = self.user.createApiKey(login, self.api_key.createApiKey[0])
        allure.attach(name="sent body", body=f"{self.api_key.createApiKey[0]}")
        allure.attach(name="response body", body=f"{cr_api.text}")
        self.checker.response_checker(cr_api.status_code, cr_api.text)

    @pytest.fixture()
    def getApiKeys(self, login, otp_gen):
        api_keys = self.user.get_api_key(login, self.api_key.get_api[0])
        allure.attach(name="param sent", body=f"{self.api_key.get_api[0]}")
        allure.attach(name="response body", body=f"{api_keys.text}")
        self.checker.response_checker(api_keys.status_code, api_keys.text)
        return api_keys.json()

    @pytest.mark.xdist_group("api_key")
    @pytest.mark.dependency(depends=["api_key"])
    def test_deleteApiKey(self, login, otp_gen,getApiKeys):
        uid = getApiKeys["result"][-1]["uid"]
        self.api_key.deleteApiKey[0]["uid"] = uid
        self.api_key.deleteApiKey[0]['otpToken'] = otp_gen
        delete_api = self.user.deleteApiKey(login, self.api_key.deleteApiKey[0])
        allure.attach(name="sent body", body=f"{self.api_key.deleteApiKey[0]}")
        allure.attach(name="response body", body=f"{delete_api.text}")
        self.checker.response_checker(delete_api.status_code, delete_api.text)