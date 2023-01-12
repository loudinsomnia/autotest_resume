import pytest
from utils.helpers.asserts import Aserts
from src.Pages.MerchantPage import AssetRecive
from utils.helpers.screenshot import Screen
from src.steps.teststep import TestSteps
from selenium.common.exceptions import TimeoutException
import allure


@pytest.mark.usefixtures("driver_init", "close_driver")
class TestRecive:
    @pytest.fixture()
    def login(self):
        step = TestSteps()
        step.login(self.driver)

    @pytest.fixture()
    def enter_merch(self):
        step = TestSteps()
        step.enter_merchant(self.driver)

    @allure.step("create_recive")
    def test_create_recive(self, login, enter_merch):
        try:
            recive = AssetRecive(self.driver)
            recive.search_asset()
            recive.open_tools()
            recive.click_recive()
            recive.add_commit()
            recive.create_recive_asset()
            asert = Aserts(self.driver)
            asert.console_checker()
            asert.create_recivewithdraw_checker()
            screen = Screen(self.driver)
            screen.create_screnshot()
        except TimeoutException:
            allure.attach(name="Time out exceprion", body="OTP validation end")
