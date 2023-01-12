import allure
import pytest
from utils.test_classAPI import User
from src.API_DATA.test_data import Assets
from utils.helpers.asserts import APIAssert
from src.steps.teststep import TestAPISteps


class TestUpdateAssets:
    user = User()
    asset = Assets()
    checker = APIAssert()
    test_step = TestAPISteps()

    @pytest.fixture()
    def login(self):
        return self.test_step.login_user()

    @pytest.mark.xdist_group(name='assetupdate')
    def test_putSymbolToAssetsList(self, login):
        put_symbol = self.user.putSymbolToAssetsList(login, self.asset.putAsetsSymbol)
        allure.attach(name="sent body", body=f"{self.asset.putAsetsSymbol}")
        allure.attach(name="response body", body=f"{put_symbol.text}")
        self.checker.response_checker(put_symbol.status_code, put_symbol.text)

    @pytest.mark.xdist_group('assetupdate')
    def test_deleteSymbolFromAssetsList(self,login):
        delete_symbol = self.user.deleteSymbolFromAssetsList(login, self.asset.deleteAssetSymbol)
        allure.attach(name="sent body", body=f"{self.asset.deleteAssetSymbol}")
        allure.attach(name="response body", body=f"{delete_symbol.text}")
        self.checker.response_checker(delete_symbol.status_code, delete_symbol.text)

