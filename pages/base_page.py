import allure
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_element_visible(self, locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def wait_for_elements_visible(self, locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_all_elements_located(locator))

    def wait_for_element_present(self, locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def wait_for_elements_present(self, locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))

    @allure.step("Переключиться на новое окно и проверить редирект")
    def switch_to_new_window_and_verify_redirect(self, expected_domains):
        main_window = self.driver.current_window_handle
        
        self.wait.until(lambda driver: len(driver.window_handles) > 1)
        
        all_windows = self.driver.window_handles
        new_window = [window for window in all_windows if window != main_window][0]
        self.driver.switch_to.window(new_window)
        
        self.wait.until(lambda driver: driver.current_url != "about:blank")
        current_url = self.driver.current_url
        
        return any(domain in current_url for domain in expected_domains)

    @allure.step("Дождаться значения элемента")
    def wait_for_element_value(self, locator, expected_value, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(lambda driver: driver.find_element(*locator).get_attribute('value') == expected_value)

    @allure.step("Дождаться количества окон")
    def wait_for_number_of_windows(self, number, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(lambda driver: len(driver.window_handles) == number)

    @allure.step("Дождаться URL содержащего любой из доменов")
    def wait_for_url_contains_any(self, domains, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(lambda driver: any(domain in driver.current_url for domain in domains))

    @allure.step("Дождаться невидимости элемента")
    def wait_for_element_not_visible(self, locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located(locator))

    def click_element(self, locator):
        element = self.wait_for_element_clickable(locator)
        element.click()

    def is_element_visible(self, locator, timeout=5):
        try:
            self.wait_for_element_visible(locator, timeout)
            return True
        except TimeoutException:
            return False

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def scroll_to_element(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def fill_field(self, locator, value):
        field = self.wait_for_element_clickable(locator)
        field.clear()
        field.send_keys(value)
        time.sleep(0.3)