import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import WebDriverException
import sys


@pytest.fixture(scope="function")
def driver():
    with allure.step("Запуск браузера Firefox"):
        driver = _create_firefox_driver()
    
    with allure.step("Максимизация окна браузера"):
        driver.maximize_window()
    
    yield driver
    
    with allure.step("Закрытие браузера"):
        driver.quit()


def _create_firefox_driver():
    try:
        service = Service()
        return webdriver.Firefox(service=service)
    except WebDriverException as e:
        return _try_webdriver_manager_fallback(e)


def _try_webdriver_manager_fallback(original_exception):
    try:
        import importlib
        importlib.import_module('webdriver_manager')
        
        from webdriver_manager.firefox import GeckoDriverManager
        service = Service(GeckoDriverManager().install())
        return webdriver.Firefox(service=service)
    except ImportError:
        error_message = (
            "Не удалось запустить Firefox WebDriver.\n"
            "Решения:\n"
            "1. Установите geckodriver и добавьте его в системную переменную PATH\n"
            "2. Или установите пакет: pip install webdriver-manager\n"
            "3. Убедитесь, что Firefox установлен в системе\n"
            f"Оригинальная ошибка: {original_exception}"
        )
        raise WebDriverException(error_message) from original_exception
    except WebDriverException as e:
        error_message = (
            "Не удалось запустить Firefox WebDriver даже через webdriver-manager.\n"
            "Убедитесь, что:\n"
            "1. Firefox установлен в системе\n" 
            "2. Имеется подключение к интернету для загрузки драйвера\n"
            f"Ошибка webdriver-manager: {e}\n"
            f"Оригинальная ошибка: {original_exception}"
        )
        raise WebDriverException(error_message) from e