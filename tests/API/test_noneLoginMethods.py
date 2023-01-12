import pytest
from utils.test_classAPI import NoneLoginMethods
from src.API_DATA.test_data import NoneLoginData
import allure
from utils.helpers.asserts import APIAssert


class TestNoneLoginMethods:

    nonelogin = NoneLoginMethods()
    nonelogindata = NoneLoginData()
    checker = APIAssert()


    def test_register(self):
        self.nonelogindata.register_data["password"] = self.nonelogindata.register_data["email"]
        register = self.nonelogin.register(self.nonelogindata.register_data)
        allure.attach(name="sent body", body=f"{self.nonelogindata.register_data}")
        allure.attach(name="response body", body=f"{register.text}")
        self.checker.nonlogin_response_register(register.status_code,register.text)


