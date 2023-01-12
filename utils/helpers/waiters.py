from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from src.Pages.driver_init import InitDriver


class Waiters(InitDriver):
    def __init__(self, driver):
        super().__init__(driver)


    def wait_clicable(self,selector, locator, time_out):
        clickable = WebDriverWait(self.driver, int(time_out)).until(
            EC.element_to_be_clickable((selector, locator)))
        return clickable

    def wait_until_visible(self, selector, locator, time_out):
        until_visible = WebDriverWait(self.driver, int(time_out)).until(
            EC.invisibility_of_element_located((selector, locator)))
        return until_visible

    def wait_tobe_visible(self, selector, locator, time_out):
        to_visible = WebDriverWait(self.driver, int(time_out)).until(
            EC.visibility_of_element_located((selector, locator)))
        return to_visible

    def find(self, selector, locator):
        element = self.driver.find_element(selector, locator)
        if element:
            return element
        else:
            return False

    def wait_until_find(self, time_out, selector, locator):
        element = WebDriverWait(self.driver, int(time_out)).until(self.find(selector, locator))
        return element