from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities as DC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import warnings
import os



class DriverInitiate:
    def browser_init(self, browser):
        if browser == "Chrome":
            PATH = (r"http://selenium__standalone-chrome:4444/wd/hub")
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--log-level=OFF')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--window-size=1920x1080')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            chrome_options.add_experimental_option("prefs", {
                "download.default_directory": r"C:\Temp",
                "download.prompt_for_download": False,
            })
            chrome_options.add_experimental_option('useAutomationExtension', False)
            ds = DC.CHROME
            ds['goog:loggingPrefs'] = {'browser': 'SEVERE'}
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                driver = webdriver.Remote(command_executor=PATH,options=chrome_options,desired_capabilities=ds)  # Git driver with services
                # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                #                           chrome_options=chrome_options,
                #                           desired_capabilities=ds)
                return driver
        else:
            firefox_option = webdriver.FirefoxOptions()
            firefox_option.set_preference("dom.webnotifications.serviceworker.enabled", False)
            firefox_option.set_preference("dom.webnotifications.enabled", False)
            firefox_option.set_preference('devtools.console.enabled', True)
            firefox_option.add_argument('--headless')
            firefox_option.add_argument('--log-level=OFF')
            firefox_option.set_capability('browser', 'SEVERE')
            firefox_option.set_preference("browser.download.folderList", 2)
            firefox_option.set_preference("browser.download.manager.showWhenStarting", False)
            firefox_option.set_preference("browser.download.dir", r"C:\Temp")
            firefox_option.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
            dc = DC.FIREFOX
            dc['goog:loggingPrefs'] = {'browser': 'SEVERE'}
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                driver = webdriver.Remote(command_executor=r"http://selenium__standalone-firefox:4444/wd/hub",options=firefox_option,
                                           desired_capabilities=dc)  # Git driver with services
                # driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=firefox_option,
                #                            desired_capabilities=dc,
                #                            service_log_path=os.devnull)  # driver for local testing
                return driver



