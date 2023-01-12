import pytest
from utils.test_classAPI import User, Admin
from src.API_DATA.test_data import USERTestData, SecretKey, Transactions, Merchant, Assets, \
    AdminMethods
from utils.helpers.asserts import APIAssert
from src.steps.teststep import TestAPISteps
import allure


class TestUser:
    admin = Admin()
    admin_methods = AdminMethods()
    user = User()
    secret = SecretKey()
    transaction = Transactions()
    merchants = Merchant()
    assets = Assets()
    checker = APIAssert()
    test_step = TestAPISteps()

    @pytest.fixture()
    def otp_gen(self):
        return self.test_step.otp_gen_user()

    @pytest.fixture()
    def login(self):
        return self.test_step.login_user()

    @allure.step("create_merchant")
    def test_create_merchant(self, login, otp_gen):
        self.merchants.createMerchant['otpToken'] = otp_gen
        merch = self.user.create_merchant(login, self.merchants.createMerchant)
        allure.attach(name="sent body", body=f"{self.merchants.createMerchant}")
        allure.attach(name="response body", body=f"{merch.text}")
        self.checker.check_to_muchmerchnat(merch.status_code, merch.text)

    @allure.step("patchMerchantSettings")
    @pytest.mark.parametrize("settings", merchants.patchMerchantSettings)
    def test_patchMerchantSettings(self, login, settings):
        settings = self.user.patchMerchantSettings(login, settings)
        allure.attach(name="response body", body=f"{settings.text}")
        self.checker.response_checker(settings.status_code, settings.text)

    @pytest.mark.xdist_group("API_Secret")
    @allure.step("putSecret")
    @pytest.mark.parametrize("merchUid", secret.putSecret)
    def test_putSecret(self, login, merchUid, otp_gen):
        merchUid['otpToken'] = otp_gen
        secret = self.user.putSecret(login, merchUid)
        allure.attach(name="sent body", body=f"{merchUid}")
        allure.attach(name="response body", body=f"{secret.text}")
        self.checker.response_checker(secret.status_code, secret.text)

    @pytest.mark.xdist_group("API_Secret")
    @pytest.mark.parametrize("merchUid", secret.deletSecret)
    @allure.step("delSecret")
    def test_delSecret(self, login, merchUid):
        del_secret = self.user.deleteSecretKey(login, merchUid)
        allure.attach(name="response body", body=f"{del_secret.text}")
        self.checker.response_checker(del_secret.status_code, del_secret.text)

    @allure.step("createPayment")
    @pytest.mark.parametrize("cr_payment", transaction.createPayment)
    def test_createPayment(self, login, cr_payment):
        payment = self.user.createPayment(login, cr_payment)
        allure.attach(name="sent body", body=f"{cr_payment}")
        allure.attach(name="response body", body=f"{payment.text}")
        self.checker.response_checker(payment.status_code, payment.text)

    @allure.step("createWithdraw")
    @pytest.mark.parametrize("cr_withdraw", transaction.createWithdraw)
    def test_createWithdraw(self, login, cr_withdraw):
        self.test_step.create_withdraw(login=login, cr_withdraw=cr_withdraw)

    @allure.step("admin_methods")
    @pytest.mark.xfail
    def test_admin_methods(self, login):
        getUsers = self.admin.getUsers(login)
        allure.attach(name="response body", body=f"{getUsers.text}")
        self.checker.response_checker(getUsers.status_code, getUsers.text)

    @pytest.mark.xfail
    def test_getUserEvents(self, login):
        event = self.admin.getUsersEvents(login)
        allure.attach(name="response body", body=f"{event.text}")
        self.checker.response_checker(event.status_code, event.text)

    @allure.step("getTransactions")
    @pytest.mark.parametrize("transaction", transaction.getTransactions)
    def test_getTransactions(self, login, transaction):
        get_transactions = self.user.getTransactions(login, transaction)
        allure.attach(name="sent body", body=f"{transaction}")
        allure.attach(name="response body", body=f"{get_transactions.text}")
        self.checker.response_checker(get_transactions.status_code, get_transactions.text)

    @allure.step("getPendings")
    @pytest.mark.parametrize("merchant", transaction.getPendings)
    def test_getPendings(self, login, merchant):
        getpending = self.user.getPendings(login, merchant)
        allure.attach(name="sent body", body=f"{merchant}")
        allure.attach(name="response body", body=f"{getpending.text}")
        self.checker.response_checker(getpending.status_code, getpending.text)

    @allure.step("bulkCreateWithdaws")
    @pytest.mark.parametrize("bastch",transaction.create_batch_transaction)
    def test_bulkCreateWithdaws(self, login,bastch):
        batch = self.user.bulkCreateWithdaws(login, bastch)
        allure.attach(name="sent body", body=f"{bastch}")
        allure.attach(name="response body", body=f"{batch.text}")
        self.checker.bulk_checker(batch.status_code, batch.text)

    @allure.step("checkWithdrawValidity")
    @pytest.mark.parametrize("check_data",transaction.checkvalid_transaction)
    def test_checkValidation(self,login,check_data):
        valid = self.user.checkValidation(login,check_data)
        allure.attach(name="sent body",body=f"{check_data}")
        allure.attach(name="Response", body=f"{valid.text}")
        self.checker.response_checker(valid.status_code,valid.text)
