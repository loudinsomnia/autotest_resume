import pytest
from src.steps.teststep import TestSteps



@pytest.mark.usefixtures("driver_init","close_driver")
class TestLogin:
    def test_login(self):
        step = TestSteps()
        step.login(self.driver)