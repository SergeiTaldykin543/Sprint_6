import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By


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

    def wait_for_element_not_visible(self, locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_element_value(self, locator, expected_value, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(lambda driver: self.find_element(locator).get_attribute('value') == expected_value)

    def wait_for_number_of_windows(self, number, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(lambda driver: len(driver.window_handles) == number)

    def wait_for_url_contains_any(self, domains, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(lambda driver: any(domain in driver.current_url for domain in domains))

    def wait_for_url_contains(self, text, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.url_contains(text))

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

    def scroll_to_element(self, locator_or_element):
        if isinstance(locator_or_element, tuple):
            element = self.find_element(locator_or_element)
        else:
            element = locator_or_element
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)

    def fill_field(self, locator, value):
        field = self.wait_for_element_clickable(locator)
        field.clear()
        
        WebDriverWait(self.driver, 5).until(lambda driver: field.get_attribute('value') == '' or field.get_attribute('value') is None)
        
        field.send_keys(value)
        
        WebDriverWait(self.driver, 5).until(lambda driver: field.get_attribute('value') == str(value))

    def get_current_url(self):
        return self.driver.current_url

    def switch_to_window(self, window_handle):
        self.driver.switch_to.window(window_handle)

    def get_window_handles(self):
        return self.driver.window_handles

    def get_current_window_handle(self):
        return self.driver.current_window_handle

    @allure.step("Переключиться на новое окно и проверить редирект")
    def switch_to_new_window_and_verify_redirect(self, expected_domains):
        main_window = self.get_current_window_handle()
        
        self.wait.until(lambda driver: len(self.get_window_handles()) > 1)
        
        all_windows = self.get_window_handles()
        new_window = [window for window in all_windows if window != main_window][0]
        self.switch_to_window(new_window)
        
        self.wait.until(lambda driver: self.get_current_url() != "about:blank")
        current_url = self.get_current_url()
        
        return any(domain in current_url for domain in expected_domains)

    def wait_for_element_fully_clickable(self, locator, timeout=10):
        element = self.wait_for_element_visible(locator, timeout)
        
        self.wait.until(lambda driver: element.is_displayed() and element.is_enabled() and self._is_element_not_obscured(element))
        return element

    def _is_element_not_obscured(self, element):
        try:
            element_rect = element.rect
            element_center_x = element_rect['x'] + element_rect['width'] / 2
            element_center_y = element_rect['y'] + element_rect['height'] / 2
            element_at_point = self.driver.execute_script(
                "return document.elementFromPoint(arguments[0], arguments[1]);",
                element_center_x, element_center_y
            )

            return element == element_at_point or element == element_at_point.find_element(By.XPATH, "./ancestor-or-self::*[. = current()]")
        except:
            return True

    def _is_element_present_and_visible(self, locator):
        try:
            element = self.find_element(locator)
            return element.is_displayed()
        except:
            return False