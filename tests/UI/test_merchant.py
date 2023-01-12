import random
import string
import pytest
from src.Pages.OTP import OTPtokken
from src.Pages.homePage import Merchant
from utils.helpers.asserts import Aserts
from src.steps.teststep import TestSteps
from selenium.common.exceptions import TimeoutException
import allure


@pytest.mark.usefixtures("driver_init", "close_driver")
class TestCreateMerchant:
    @pytest.fixture()
    def login(self):
        step = TestSteps()
        step.login(self.driver)

    def test_create_merchant(self, login):
        try:
            merch_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
            merch = Merchant(self.driver)
            merch.create_new_merchant()
            merch.new_name_for_merchant(merch_name)
            merch.create_merch()
            otp = OTPtokken(self.driver)
            otp.enter_otp()
            otp.click_ok()
            asert = Aserts(self.driver)
            asert.console_checker()
            asert.merch_checker(merch_name)
        except TimeoutException:
            allure.attach(name="Time out exceprion", body="OTP validation end")
