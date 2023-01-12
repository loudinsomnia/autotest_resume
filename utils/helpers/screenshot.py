import allure
from src.Pages.driver_init import InitDriver

class Screen(InitDriver):
    def __init__(self, driver):
        super().__init__(driver)

    def create_screnshot(self):
        allure.attach(self.driver.get_screenshot_as_png(), name="LoginPage", attachment_type=allure.attachment_type.PNG)