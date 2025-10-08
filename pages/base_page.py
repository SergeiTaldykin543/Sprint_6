import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from abc import ABC, abstractmethod


class BasePage(ABC):
    def __init__(self, driver):
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)

    # === Приватные методы для инкапсуляции драйвера ===
    def _get_driver(self):
        return self._driver

    def _get_wait(self, timeout=None):
        if timeout is None:
            return self._wait
        return WebDriverWait(self._driver, timeout)

    def _execute_script(self, script, *args):
        return self._driver.execute_script(script, *args)

    # === Базовые методы навигации ===
    def open_url(self, url):
        self._driver.get(url)

    def refresh_page(self):
        self._driver.refresh()

    def get_current_url(self):
        return self._driver.current_url

    def get_page_title(self):
        return self._driver.title

    # === Базовые методы работы с элементами ===
    def find_element(self, locator):
        return self._driver.find_element(*locator)

    def find_elements(self, locator):
        return self._driver.find_elements(*locator)

    def click_element(self, locator):
        element = self.wait_for_element_clickable(locator)
        element.click()

    def send_keys_to_element(self, locator, text):
        element = self.wait_for_element_clickable(locator)
        element.clear()
        element.send_keys(text)

    def get_element_text(self, locator):
        element = self.wait_for_element_visible(locator)
        return element.text

    def get_element_attribute(self, locator, attribute):
        element = self.wait_for_element_present(locator)
        return element.get_attribute(attribute)

    def is_element_selected(self, locator):
        element = self.wait_for_element_present(locator)
        return element.is_selected()

    def is_element_displayed(self, locator):
        try:
            element = self.find_element(locator)
            return element.is_displayed()
        except:
            return False

    def is_element_enabled(self, locator):
        try:
            element = self.find_element(locator)
            return element.is_enabled()
        except:
            return False

    # === Методы ожидания ===
    def wait_for_element_visible(self, locator, timeout=10):
        wait = self._get_wait(timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator, timeout=10):
        wait = self._get_wait(timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def wait_for_elements_visible(self, locator, timeout=10):
        wait = self._get_wait(timeout)
        return wait.until(EC.visibility_of_all_elements_located(locator))

    def wait_for_element_present(self, locator, timeout=10):
        wait = self._get_wait(timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def wait_for_elements_present(self, locator, timeout=10):
        wait = self._get_wait(timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))

    def wait_for_element_not_visible(self, locator, timeout=10):
        wait = self._get_wait(timeout)
        return wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_element_value(self, locator, expected_value, timeout=10):
        wait = self._get_wait(timeout)
        return wait.until(lambda driver: self.get_element_attribute(locator, 'value') == str(expected_value))

    def wait_for_text_in_element(self, locator, text, timeout=10):
        wait = self._get_wait(timeout)
        return wait.until(EC.text_to_be_present_in_element(locator, text))

    # === Методы ожидания для страницы ===
    def wait_for_url_contains(self, text, timeout=10):
        wait = self._get_wait(timeout)
        return wait.until(EC.url_contains(text))

    def wait_for_url_contains_any(self, domains, timeout=10):
        wait = self._get_wait(timeout)
        return wait.until(lambda driver: any(domain in driver.current_url for domain in domains))

    def wait_for_number_of_windows(self, number, timeout=10):
        wait = self._get_wait(timeout)
        return wait.until(lambda driver: len(driver.window_handles) == number)

    # === Методы проверки состояния ===
    def is_element_visible(self, locator, timeout=5):
        try:
            self.wait_for_element_visible(locator, timeout)
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator, timeout=5):
        try:
            self.wait_for_element_present(locator, timeout)
            return True
        except TimeoutException:
            return False

    def is_element_clickable(self, locator, timeout=5):
        try:
            self.wait_for_element_clickable(locator, timeout)
            return True
        except TimeoutException:
            return False

    # === Методы управления окнами и фреймами ===
    def switch_to_window(self, window_handle):
        self._driver.switch_to.window(window_handle)

    def get_window_handles(self):
        return self._driver.window_handles

    def get_current_window_handle(self):
        return self._driver.current_window_handle

    def switch_to_default_content(self):
        self._driver.switch_to.default_content()

    def switch_to_frame(self, frame_reference):
        self._driver.switch_to.frame(frame_reference)

    # === Сложные взаимодействия ===
    def scroll_to_element(self, locator):
        """Скролл к элементу по локатору"""
        element = self.find_element(locator)
        self._execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)

    def scroll_to_webelement(self, element):
        """Скролл к готовому WebElement"""
        self._execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)

    def scroll_to_top(self):
        self._execute_script("window.scrollTo(0, 0);")

    def scroll_to_bottom(self):
        self._execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def press_escape_key(self, locator):
        element = self.wait_for_element_clickable(locator)
        element.send_keys(Keys.ESCAPE)

    def press_enter_key(self, locator):
        element = self.wait_for_element_clickable(locator)
        element.send_keys(Keys.ENTER)

    def clear_field(self, locator):
        element = self.wait_for_element_clickable(locator)
        element.clear()

    # === Комплексные методы ===
    def fill_field_with_verification(self, locator, value):
        self.clear_field(locator)
        self.send_keys_to_element(locator, value)
        self.wait_for_element_value(locator, value)

    def click_with_retry(self, locator, retries=2):
        for attempt in range(retries + 1):
            try:
                self.click_element(locator)
                return
            except StaleElementReferenceException:
                if attempt == retries:
                    raise
                continue

    def select_checkbox(self, locator):
        if not self.is_element_selected(locator):
            self.click_element(locator)

    def unselect_checkbox(self, locator):
        if self.is_element_selected(locator):
            self.click_element(locator)

    # === Методы для работы с текстом элементов (без локаторов) ===
    def get_text_from_webelement(self, element):
        """Получить текст из WebElement (не из локатора)"""
        return element.text

    def click_webelement(self, element):
        """Кликнуть по WebElement (не по локатору)"""
        element.click()

    def is_webelement_displayed(self, element):
        """Проверить отображение WebElement (не локатора)"""
        return element.is_displayed()

    @allure.step("Переключиться на новое окно и проверить редирект")
    def switch_to_new_window_and_verify_redirect(self, expected_domains):
        main_window = self.get_current_window_handle()
        
        self.wait_for_number_of_windows(2)
        
        all_windows = self.get_window_handles()
        new_window = [window for window in all_windows if window != main_window][0]
        self.switch_to_window(new_window)
        
        # Исправляем использование wait
        wait = self._get_wait(10)
        wait.until(lambda driver: self.get_current_url() != "about:blank")
        
        current_url = self.get_current_url()
        return any(domain in current_url for domain in expected_domains)

    # === Абстрактные методы ===
    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def is_page_loaded(self):
        pass