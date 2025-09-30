import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import os


@pytest.fixture(scope="function")
def driver():
    with allure.step("Запуск браузера Firefox"):
        try:
            service = Service()
            driver = webdriver.Firefox(service=service)
        except Exception as e:
            geckodriver_path = "C:/WebDriver/geckodriver.exe"
            
            if os.path.exists(geckodriver_path):
                service = Service(geckodriver_path)
                driver = webdriver.Firefox(service=service)
            else:
                try:
                    from selenium.webdriver.chrome.service import Service as ChromeService
                    from webdriver_manager.chrome import ChromeDriverManager
                    
                    service = ChromeService(ChromeDriverManager().install())
                    driver = webdriver.Chrome(service=service)
                except:
                    raise Exception("Cannot create any WebDriver. Please install Firefox or Chrome driver manually.")
    
    driver.maximize_window()
    
    yield driver
    
    with allure.step("Закрытие браузера"):
        driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            try:
                screenshot = driver.get_screenshot_as_png()
                
                allure.attach(
                    screenshot,
                    name="screenshot_on_failure",
                    attachment_type=allure.attachment_type.PNG
                )
                
                page_source = driver.page_source
                allure.attach(
                    page_source,
                    name="page_source_on_failure", 
                    attachment_type=allure.attachment_type.HTML
                )
                
            except Exception as e:
                pass