import pytest
from utils.test_classUI import DriverInitiate
import os



@pytest.fixture(scope="class")
def driver_init(request):
    driver = DriverInitiate().browser_init(request.param)
    request.cls.driver = driver
    return driver



@pytest.fixture(scope="class")
def close_driver(driver_init):
    yield
    driver_init.delete_all_cookies()
    driver_init.quit()
