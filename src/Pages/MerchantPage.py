from selenium.webdriver.common.by import By
from utils.helpers.waiters import Waiters
from selenium.webdriver.common.action_chains import ActionChains
from .driver_init import InitDriver
import time

wait = Waiters


class BaseAssetsPage(InitDriver):
    def __init__(self, driver):
        super().__init__(driver)

        self.search = '//input["Search"]'
        self.tools = '//span[text()="Tools"]'
        self.recive = '//span[text()=" Receive "]'
        self.comment = '//textarea[@aria-label="Comment"]'
        self.create_recive = '// span[text() = "Create"]'
        self.recive_wallet = '//div[text()=" Address: "]//span'
        self.withdraw = '//span[text()=" Withdraw "]'
        self.withdraw_adress = '//textarea[@aria-label="Withdraw address"]'
        self.amount = '//input[@type="number"]'
        self.cr_withdraw = '//span[contains(text(),"Withdraw")]'
        self.exit_from_assetresive_window = '//span[text()="Ok"]'
        self.exit_from_assetwithdraw_window = '//span[text()="OK"]'

    def search_asset(self):
        search = wait(self.driver).wait_tobe_visible(By.XPATH, self.search, "10")
        search.clear()
        search.send_keys("BTC-test")

    def open_tools(self):
        wait(self.driver).wait_clicable(By.XPATH, self.tools, "60").click()

    def exit_from_resivewindow(self):
        wait(self.driver).wait_clicable(By.XPATH, self.exit_from_assetresive_window, "60").click()

    def exit_from_withdraw_window(self):
        wait(self.driver).wait_clicable(By.XPATH, self.exit_from_assetwithdraw_window, "60").click()


class AssetRecive(BaseAssetsPage):

    def click_recive(self):
        wait(self.driver).wait_clicable(By.XPATH, self.recive, "60").click()

    def add_commit(self):
        wait(self.driver).wait_clicable(By.XPATH, self.comment, "60").send_keys("test")

    def create_recive_asset(self):
        wait(self.driver).wait_clicable(By.XPATH, self.create_recive, "60").click()

    def parse_recive_wallet(self):
        wallet = wait(self.driver).wait_tobe_visible(By.XPATH, self.recive_wallet, "60")
        return wallet.text


class AssetWithdraw(BaseAssetsPage):

    def click_withdraw(self):
        withdraw_button = wait(self.driver).wait_clicable(By.XPATH, self.withdraw, "60")
        chain = ActionChains(self.driver)
        chain.move_to_element(withdraw_button)
        chain.click(withdraw_button)
        chain.perform()

    def add_withdraw_address(self,wallet):
        wait(self.driver).wait_tobe_visible(By.XPATH, self.withdraw_adress, "60").send_keys(wallet)  # "tb1ql7w62elx9ucw4pj5lgw4l028hmuw80sndtntxt"

    def summ_of_withdraw(self):
        summ = wait(self.driver).wait_tobe_visible(By.XPATH, self.amount, "60")
        summ.clear()
        summ.send_keys("1")

    def create_withdraw(self):
        wait(self.driver).wait_clicable(By.XPATH, self.cr_withdraw, "60").click()
