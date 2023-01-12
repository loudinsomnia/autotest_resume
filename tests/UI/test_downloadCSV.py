import time
import pytest
import os
from utils.helpers.asserts import Aserts
from src.steps.teststep import TestSteps
from src.Pages.Transactions import ExportCSV
from selenium.common.exceptions import TimeoutException
import allure


@pytest.mark.usefixtures("driver_init", "close_driver")
class TestDownloadCSV:
    @pytest.fixture()
    def login(self):
        step = TestSteps()
        step.login(self.driver)

    @pytest.fixture()
    def enter_merch(self):
        step = TestSteps()
        step.enter_merchant(self.driver)

    def test_download_csv(self,login,enter_merch):
        try:
            download = ExportCSV(self.driver)
            download.open_transactions()
            download.click_export()
            download.download_csv()
            asert = Aserts(self.driver)
            asert.console_checker()
            time.sleep(2)
            asert.download_checker()
            os.remove(r"C:\Temp\AlfaBit CoinApiReport.csv")
        except TimeoutException:
            allure.attach(name="Time out exceprion", body="OTP validation end")
