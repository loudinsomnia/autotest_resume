import time
import pytest
from src.Pages.MerchantPage import AssetRecive, AssetWithdraw
from utils.helpers.asserts import Aserts
from utils.helpers.screenshot import Screen
from src.steps.teststep import TestSteps
from selenium.common.exceptions import TimeoutException
import allure


@pytest.mark.usefixtures("driver_init", "close_driver")
class TestWithdraw:
    @pytest.fixture()
    def login(self):
        step = TestSteps()
        step.login(self.driver)

    @pytest.fixture()
    def enter_merch(self):
        step = TestSteps()
        step.enter_merchant(self.driver)

    @pytest.fixture()
    def create_recive(self):
        try:
            recive = AssetRecive(self.driver)
            recive.search_asset()
            recive.open_tools()
            recive.click_recive()
            recive.add_commit()
            recive.create_recive_asset()
            wallet = recive.parse_recive_wallet()
            asert = Aserts(self.driver)
            asert.console_checker()
            asert.create_recivewithdraw_checker()
            recive.exit_from_resivewindow()
            return wallet
        except TimeoutException:
            allure.attach(name="Time out exceprion", body="OTP validation end")

    @allure.step("create_withdraw")
    def test_create_withdraw(self, login, enter_merch, create_recive):
        try:
            withdraw = AssetWithdraw(self.driver)
            asert = Aserts(self.driver)
            time.sleep(2)
            withdraw.open_tools()
            withdraw.click_withdraw()
            withdraw.add_withdraw_address(create_recive)
            withdraw.summ_of_withdraw()
            asert.withdraw_amount()
            withdraw.create_withdraw()
            asert.console_checker()
            asert.create_recivewithdraw_checker()
            screen = Screen(self.driver)
            screen.create_screnshot()
        except TimeoutException:
            allure.attach(name="Time out exceprion", body="OTP validation end")
