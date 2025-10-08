from selenium.webdriver.common.by import By
from .base_page import BasePage
import urls
import allure


class OrderPage(BasePage):
    # Personal info section locators
    FIRST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Имя']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_STATION_INPUT = (By.XPATH, "//input[@placeholder='* Станция метро']")
    PHONE_INPUT = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.CLASS_NAME, "Button_Middle__1CSJM")

    # Rental info section locators
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

    # Additional locators
    METRO_DROPDOWN_OPTIONS = (By.CLASS_NAME, "select-search__row")
    CALENDAR = (By.CLASS_NAME, "react-datepicker")
    SCOOTER_LOGO = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
    COOKIE_BANNER = (By.CLASS_NAME, "App_CookieConsent__1yUIN")
    COOKIE_CONFIRM_BUTTON = (By.ID, "rcc-confirm-button")
    ORDER_HEADER = (By.CLASS_NAME, "Order_Header__BZXOb")
    ORDER_MODAL = (By.XPATH, "//div[contains(@class, 'Order_Modal')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = urls.ORDER_PAGE_URL

    @allure.step("Открыть страницу заказа")
    def open(self):
        self.open_url(self.url)
        self.wait_for_element_visible(self.ORDER_HEADER)
        self.close_cookie_banner()

    @allure.step("Проверить загрузку страницы заказа")
    def is_page_loaded(self):
        return self.get_current_url() == urls.ORDER_PAGE_URL

    @allure.step("Дождаться загрузки формы заказа")
    def wait_for_order_form_loaded(self):
        self.wait_for_element_visible(self.FIRST_NAME_INPUT)
        self.wait_for_element_clickable(self.FIRST_NAME_INPUT)

    @allure.step("Закрыть cookie-баннер")
    def close_cookie_banner(self):
        if self.is_element_visible(self.COOKIE_BANNER):
            self.click_element(self.COOKIE_CONFIRM_BUTTON)
            self.wait_for_element_not_visible(self.COOKIE_BANNER)

    @allure.step("Заполнить полную форму заказа")
    def fill_complete_order_form(self, order_data):
        personal_info = order_data['personal_info']
        self.fill_personal_info(
            personal_info['first_name'],
            personal_info['last_name'],
            personal_info['address'],
            personal_info['metro_station'],
            personal_info['phone']
        )
        self.click_next_button()
        
        rental_info = order_data['rental_info']
        self.fill_rental_info(
            rental_info['date'],
            rental_info['rental_period'],
            rental_info['color'],
            rental_info['comment']
        )
        self.click_order_button()
        self.confirm_order()

    @allure.step("Заполнить личную информацию")
    def fill_personal_info(self, first_name, last_name, address, metro_station, phone):
        self.fill_field_with_verification(self.FIRST_NAME_INPUT, first_name)
        self.fill_field_with_verification(self.LAST_NAME_INPUT, last_name)
        self.fill_field_with_verification(self.ADDRESS_INPUT, address)
        self.fill_field_with_verification(self.PHONE_INPUT, phone)
        self.select_metro_station(metro_station)

    @allure.step("Выбрать станцию метро: '{station_name}'")
    def select_metro_station(self, station_name):
        self.scroll_to_element(self.METRO_STATION_INPUT)
        self.click_element(self.METRO_STATION_INPUT)
        self.wait_for_element_visible(self.METRO_DROPDOWN_OPTIONS)
        
        self.send_keys_to_element(self.METRO_STATION_INPUT, station_name)
        
        station_options = self.wait_for_elements_present(self.METRO_DROPDOWN_OPTIONS)
        if station_options:
            self.click_element(station_options[0])

    @allure.step("Нажать кнопку 'Далее'")
    def click_next_button(self):
        self.close_cookie_banner()
        self.scroll_to_element(self.NEXT_BUTTON)
        self.click_element(self.NEXT_BUTTON)
        self.wait_for_second_page()

    @allure.step("Дождаться загрузки второй страницы формы")
    def wait_for_second_page(self):
        self.wait_for_element_visible(self.RENTAL_HEADER)

    @allure.step("Заполнить информацию об аренде")
    def fill_rental_info(self, date, rental_period, color, comment):
        self.fill_field_with_verification(self.DATE_INPUT, date)
        self.close_calendar_if_visible()
        self.select_rental_period(rental_period)
        
        if color == "black":
            self.select_checkbox(self.COLOR_BLACK_CHECKBOX)
        elif color == "grey":
            self.select_checkbox(self.COLOR_GREY_CHECKBOX)
            
        if comment:
            self.fill_field_with_verification(self.COMMENT_INPUT, comment)

    @allure.step("Выбрать период аренды: '{rental_period}'")
    def select_rental_period(self, rental_period):
        self.scroll_to_element(self.RENTAL_PERIOD_DROPDOWN)
        self.click_element(self.RENTAL_PERIOD_DROPDOWN)
        
        options = self.wait_for_elements_visible(self.RENTAL_PERIOD_OPTIONS)
        for option in options:
            # Используем новый метод для работы с WebElement
            option_text = self.get_text_from_webelement(option)
            if rental_period in option_text:
                # Используем новый метод для скролла к WebElement
                self.scroll_to_webelement(option)
                self.click_webelement(option)  # Используем метод для WebElement
                return
                
        if options:
            self.click_webelement(options[0])  # Используем метод для WebElement

    @allure.step("Закрыть календарь если открыт")
    def close_calendar_if_visible(self):
        if self.is_element_visible(self.CALENDAR):
            self.press_escape_key(self.DATE_INPUT)
            self.wait_for_element_not_visible(self.CALENDAR)

    @allure.step("Нажать кнопку 'Заказать'")
    def click_order_button(self):
        self.close_cookie_banner()
        self.scroll_to_element(self.ORDER_BUTTON)
        self.click_element(self.ORDER_BUTTON)

    @allure.step("Подтвердить заказ")
    def confirm_order(self):
        self.wait_for_element_visible(self.ORDER_MODAL)
        self.scroll_to_element(self.CONFIRM_ORDER_BUTTON)
        self.click_element(self.CONFIRM_ORDER_BUTTON)
        self.wait_for_element_visible(self.SUCCESS_MESSAGE)

    @allure.step("Проверить отображение сообщения об успехе")
    def is_success_message_displayed(self):
        return self.is_element_visible(self.SUCCESS_MESSAGE)

    @allure.step("Нажать логотип Самоката")
    def click_scooter_logo(self):
        self.click_element(self.SCOOTER_LOGO)