import pytest
from utils.helpers.asserts import APIAssert
from utils.test_classAPI import Public, API
from src.API_DATA.test_data import APITestData, Merchant, APIKey
import allure


class TestAPI:
    public = Public()
    api = API()
    api_key = APIKey()

    @allure.step("public_info")
    def test_public_info(self):
        public_info = self.public.get_Info()
        allure.attach(name="response body", body=f"{public_info.text}")
        APIAssert().response_checker(public_info.status_code, public_info.text)

    @allure.step("public_AssetsList")
    def test_public_AssetsList(self):
        AssetsList = self.public.getAssetsList()
        allure.attach(name="response body", body=f"{AssetsList.text}")
        APIAssert().response_checker(AssetsList.status_code, AssetsList.text)

    @allure.step("get_Merchant")
    @pytest.mark.xfail()
    def test_get_Merchant(self):
        Merchants = self.api.getMerchants()
        allure.attach(name="response body", body=f"{Merchants.text}")
        APIAssert().response_checker(Merchants.status_code, Merchants.text)

    @allure.step("getMerchantWallets")
    def test_getMerchantWallets(self):
        wallet = self.api.getMerchantWallets(Merchant.getWallets)
        allure.attach(name="response body", body=f"{wallet.text}")
        APIAssert().response_checker(wallet.status_code, wallet.text)

    @allure.step("getMerchantPendings")
    def test_getMerchantPendings(self):
        pending = self.api.getMerchantPendings(Merchant.getWallets)
        allure.attach(name="response body", body=f"{pending.text}")
        APIAssert().response_checker(pending.status_code, pending.text)

    @allure.step("getMerchantBalances")
    def test_getMerchantBalances(self):
        balance = self.api.getMerchantBalances(Merchant.getWallets)
        allure.attach(name="response body", body=f"{balance.text}")
        APIAssert().response_checker(balance.status_code, balance.text)


    @allure.step("cr_withdraw")
    @pytest.mark.parametrize("data_cr_withdraw", APITestData.withdraw_data)
    def test_cr_withdraw(self, data_cr_withdraw):
        withdraw = self.api.createWithdraw(data_cr_withdraw)
        allure.attach(name="response body", body=f"{withdraw.text}")
        APIAssert().response_checker(withdraw.status_code, withdraw.text)

    @allure.step("cr_recive")
    @pytest.mark.parametrize("data_cr_recive", APITestData.payment_data)
    def test_cr_recive(self, data_cr_recive):
        recive = self.api.createRecive(data_cr_recive)
        allure.attach(name="response body", body=f"{recive.text}")
        APIAssert().response_checker(recive.status_code, recive.text)

    @allure.step("createApiKey")
    @pytest.mark.xfail()
    @pytest.mark.parametrize("api_key",api_key.createApiKey)
    def test_createApiKey(self,api_key):
        cr_api = self.api.createApiKey(api_key)
        allure.attach(name="sent body", body=f"{self.api_key.createApiKey[0]}")
        allure.attach(name="response body", body=f"{cr_api.text}")
        APIAssert().response_checker(cr_api.status_code, cr_api.text)
