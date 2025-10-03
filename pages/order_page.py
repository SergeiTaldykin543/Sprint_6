from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import urls
import allure


class OrderPage(BasePage):
    FIRST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Имя']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_STATION_INPUT = (By.XPATH, "//input[@placeholder='* Станция метро']")
    PHONE_INPUT = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.CLASS_NAME, "Button_Middle__1CSJM")

    ERROR_MESSAGES = (By.CLASS_NAME, "Input_ErrorMessage__3HvIb")

    RENTAL_HEADER = (By.XPATH, "//div[contains(text(), 'Про аренду')]")
    DATE_INPUT = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    RENTAL_PERIOD_DROPDOWN = (By.CLASS_NAME, "Dropdown-placeholder")
    RENTAL_PERIOD_OPTIONS = (By.CLASS_NAME, "Dropdown-option")
    COLOR_BLACK_CHECKBOX = (By.ID, "black")
    COLOR_GREY_CHECKBOX = (By.ID, "grey")
    COMMENT_INPUT = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Заказать') and @class='Button_Button__ra12g Button_Middle__1CSJM']")
    CONFIRM_ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Да')]")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "Order_ModalHeader__3FDaJ")

    METRO_DROPDOWN_OPTIONS = (By.CLASS_NAME, "select-search__row")
    METRO_OPTION_BUTTON = (By.XPATH, ".//button")

    CALENDAR = (By.CLASS_NAME, "react-datepicker")
    SCOOTER_LOGO = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
    
    # Локаторы для cookie-баннера
    COOKIE_BANNER = (By.CLASS_NAME, "App_CookieConsent__1yUIN")
    COOKIE_CONFIRM_BUTTON = (By.ID, "rcc-confirm-button")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = urls.ORDER_PAGE_URL

    @allure.step("Открыть страницу заказа")
    def open(self):
        self.driver.get(self.url)
        self.wait_for_element_visible((By.CLASS_NAME, "Order_Header__BZXOb"))
        self.close_cookie_banner()

    @allure.step("Дождаться загрузки формы заказа")
    def wait_for_order_form_loaded(self):
        form_elements = [
            self.FIRST_NAME_INPUT,
            self.LAST_NAME_INPUT,
            self.ADDRESS_INPUT,
            (By.CLASS_NAME, "Order_Header__BZXOb")]
        
        for element_locator in form_elements:
            self.wait_for_element_visible(element_locator)
        
        self.wait.until(lambda driver: driver.find_element(*self.FIRST_NAME_INPUT).is_enabled())

    @allure.step("Закрыть cookie-баннер")
    def close_cookie_banner(self):
        try:
            cookie_banner = self.find_elements(self.COOKIE_BANNER)
            if cookie_banner and cookie_banner[0].is_displayed():
                confirm_button = self.wait_for_element_clickable(self.COOKIE_CONFIRM_BUTTON)
                confirm_button.click()
                self.wait_for_element_not_visible(self.COOKIE_BANNER)
        except Exception:
            pass

    @allure.step("Заполнить полную форму заказа")
    def fill_complete_order_form(self, order_data):
        personal_info = order_data['personal_info']
        
        self.fill_personal_info_simple(
            personal_info['first_name'],
            personal_info['last_name'],
            personal_info['address'],
            personal_info['metro_station'],
            personal_info['phone'])

        self.click_next_button_safe()

        rental_info = order_data['rental_info']
        self.fill_rental_info(
            rental_info['date'],
            rental_info['rental_period'],
            rental_info['color'],
            rental_info['comment'])
        
        self.click_order_button_safe()
        self.confirm_order_safe()

    @allure.step("Заполнить личную информацию (упрощенная версия)")
    def fill_personal_info_simple(self, first_name, last_name, address, metro_station, phone):
        self.fill_field_safe(self.FIRST_NAME_INPUT, first_name)
        self.fill_field_safe(self.LAST_NAME_INPUT, last_name)
        self.fill_field_safe(self.ADDRESS_INPUT, address)
        self.fill_field_safe(self.PHONE_INPUT, phone)
        
        self.select_metro_station_safe(metro_station)

    @allure.step("Заполнить поле: {value}")
    def fill_field_safe(self, locator, value):
        field = self.wait_for_element_clickable(locator)
        field.clear()
        field.send_keys(value)
        self.wait_for_element_value(locator, value)

    @allure.step("Выбрать станцию метро: '{station_name}' (безопасная версия)")
    def select_metro_station_safe(self, station_name):
        metro_field = self.wait_for_element_clickable(self.METRO_STATION_INPUT)
        
        self.scroll_to_element_safe(self.METRO_STATION_INPUT)
        metro_field.click()
        
        self.wait_for_element_visible(self.METRO_DROPDOWN_OPTIONS)
        
        metro_field.send_keys(station_name)
        
        self.wait_for_elements_present(self.METRO_DROPDOWN_OPTIONS)
        station_options = self.find_elements(self.METRO_DROPDOWN_OPTIONS)
        
        if station_options:
            first_option = station_options[0]
            button = first_option.find_element(*self.METRO_OPTION_BUTTON)
            self.scroll_to_element_safe(button)
            button.click()

    @allure.step("Нажать кнопку 'Далее' (безопасная версия)")
    def click_next_button_safe(self):
        self.close_cookie_banner()
        self.scroll_to_element_safe(self.NEXT_BUTTON)

        next_button = self.wait_for_element_fully_clickable(self.NEXT_BUTTON)
        next_button.click()
        
        self.wait_for_second_page()

    def scroll_to_element_safe(self, locator_or_element):
        if isinstance(locator_or_element, tuple):
            element = self.find_element(locator_or_element)
        else:
            element = locator_or_element
            
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)

    def wait_for_element_fully_clickable(self, locator, timeout=10):
        element = self.wait_for_element_visible(locator, timeout)
        
        self.wait.until(lambda driver: element.is_displayed() and element.is_enabled() and self._is_element_not_obscured(element))
        return element

    def _is_element_not_obscured(self, element):
        try:
            element_rect = element.rect
            element_center_x = element_rect['x'] + element_rect['width'] / 2
            element_center_y = element_rect['y'] + element_rect['height'] / 2
            element_at_point = self.driver.execute_script("return document.elementFromPoint(arguments[0], arguments[1]);",element_center_x, element_center_y)

            return element == element_at_point or element == element_at_point.find_element(By.XPATH, "./ancestor-or-self::*[. = current()]")
        except:
            return True

    def wait_for_second_page(self):
        self.wait.until(
            lambda driver: any([
                self._is_element_present_and_visible(self.RENTAL_HEADER),
                self._is_element_present_and_visible(self.DATE_INPUT),
                self._is_element_present_and_visible(self.RENTAL_PERIOD_DROPDOWN)]))

    def _is_element_present_and_visible(self, locator):
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except:
            return False

    @allure.step("Заполнить информацию об аренде")
    def fill_rental_info(self, date, rental_period, color, comment):
        self.fill_field_safe(self.DATE_INPUT, date)
        self.close_calendar_if_visible()
        self.select_rental_period_safe(rental_period)
        if color == "black":
            self.click_checkbox_safe(self.COLOR_BLACK_CHECKBOX)
        elif color == "grey":
            self.click_checkbox_safe(self.COLOR_GREY_CHECKBOX)
        if comment:
            self.fill_field_safe(self.COMMENT_INPUT, comment)

    @allure.step("Выбрать период аренды: '{rental_period}' (безопасная версия)")
    def select_rental_period_safe(self, rental_period):
        self.scroll_to_element_safe(self.RENTAL_PERIOD_DROPDOWN)
        dropdown = self.wait_for_element_fully_clickable(self.RENTAL_PERIOD_DROPDOWN)
        dropdown.click()
        options = self.wait_for_elements_visible(self.RENTAL_PERIOD_OPTIONS)
        
        for option in options:
            if rental_period in option.text:
                self.scroll_to_element_safe(option)
                clickable_option = self.wait_for_element_fully_clickable((By.XPATH, f"//div[contains(@class, 'Dropdown-option') and contains(text(), '{rental_period}')]"))
                clickable_option.click()
                return             
        if options:
            self.scroll_to_element_safe(options[0])
            clickable_first_option = self.wait_for_element_fully_clickable(self.RENTAL_PERIOD_OPTIONS)
            clickable_first_option.click()

    @allure.step("Нажать чекбокс")
    def click_checkbox_safe(self, locator):
        checkbox = self.wait_for_element_fully_clickable(locator)
        if not checkbox.is_selected():
            self.scroll_to_element_safe(locator)
            checkbox.click()

    @allure.step("Закрыть календарь если открыт")
    def close_calendar_if_visible(self):
        try:
            calendar = self.find_elements(self.CALENDAR)
            if calendar and calendar[0].is_displayed():
                date_field = self.find_element(self.DATE_INPUT)
                date_field.send_keys(Keys.ESCAPE)
                self.wait.until(EC.invisibility_of_element_located(self.CALENDAR))
        except Exception:
            pass

    @allure.step("Нажать кнопку 'Заказать' (безопасная версия)")
    def click_order_button_safe(self):
        self.close_cookie_banner()
        self.scroll_to_element_safe(self.ORDER_BUTTON)
        order_button = self.wait_for_element_fully_clickable(self.ORDER_BUTTON)
        order_button.click()

    @allure.step("Подтвердить заказ (безопасная версия)")
    def confirm_order_safe(self):
        self.wait_for_element_visible((By.XPATH, "//div[contains(@class, 'Order_Modal')]"))
        self.scroll_to_element_safe(self.CONFIRM_ORDER_BUTTON)
        confirm_button = self.wait_for_element_fully_clickable(self.CONFIRM_ORDER_BUTTON)
        confirm_button.click()
        self.wait_for_element_visible(self.SUCCESS_MESSAGE)

    @allure.step("Проверить отображение сообщения об успехе")
    def is_success_message_displayed(self):
        return self.is_element_visible(self.SUCCESS_MESSAGE)

    @allure.step("Нажать логотип Самоката")
    def click_scooter_logo(self):
        self.click_element(self.SCOOTER_LOGO)

    @allure.step("Нажать кнопку 'Далее'")
    def click_next_button_simple(self):
        return self.click_next_button_safe()

    @allure.step("Заполнить личную информацию")
    def fill_personal_info(self, first_name, last_name, address, metro_station, phone):
        return self.fill_personal_info_simple(first_name, last_name, address, metro_station, phone)
