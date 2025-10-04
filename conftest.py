import pytest
import allure
from browser_factory import create_firefox_driver


@pytest.fixture(scope="function")
def driver():
    with allure.step("Запуск браузера Firefox"):
        driver = create_firefox_driver()
    
    with allure.step("Максимизация окна браузера"):
        driver.maximize_window()
    
    yield driver
    
    with allure.step("Закрытие браузера"):
        driver.quit()