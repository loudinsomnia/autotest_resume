import pytest
from utils.test_classUI import DriverInitiate
import os
from src.drivers import drivers
from utils.configuration import DeployConfig
from pluggy import HookspecMarker

config = DeployConfig()
hookspec = HookspecMarker("pytest")

def pytest_sessionstart(session):
    global config



@pytest.fixture(scope="class",params=drivers)
def driver_init(request):
    driver = DriverInitiate().browser_init(request.param)
    request.cls.driver = driver
    return driver



@pytest.fixture(scope="class")
def close_driver(driver_init):
    yield
    driver_init.delete_all_cookies()
    driver_init.quit()
