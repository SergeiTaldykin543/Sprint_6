from selenium.webdriver.common.by import By
from .base_page import BasePage
import urls


class OrderPage(BasePage):
    # Локаторы формы заказа
    FIRST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Имя']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_STATION_INPUT = (By.XPATH, "//input[@placeholder='* Станция метро']")
    PHONE_INPUT = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.CLASS_NAME, "Button_Middle__1CSJM")

    # Локаторы для второй части формы
    DATE_INPUT = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    RENTAL_PERIOD_DROPDOWN = (By.CLASS_NAME, "Dropdown-placeholder")
    RENTAL_PERIOD_OPTION = (By.XPATH, "//div[@class='Dropdown-option']")
    COLOR_BLACK_CHECKBOX = (By.ID, "black")
    COLOR_GREY_CHECKBOX = (By.ID, "grey")
    COMMENT_INPUT = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Заказать')]")
    CONFIRM_ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Да')]")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "Order_ModalHeader__3FDaJ")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = urls.ORDER_PAGE_URL

    def open(self):
        self.driver.get(self.url)

    def fill_personal_info(self, first_name, last_name, address, metro_station, phone):
        self.input_text(self.FIRST_NAME_INPUT, first_name)
        self.input_text(self.LAST_NAME_INPUT, last_name)
        self.input_text(self.ADDRESS_INPUT, address)
        self.input_text(self.METRO_STATION_INPUT, metro_station)
        # Выбор станции метро
        metro_option = (By.XPATH, f"//button[contains(text(), '{metro_station}')]")
        self.click_element(metro_option)
        self.input_text(self.PHONE_INPUT, phone)

    def click_next_button(self):
        self.click_element(self.NEXT_BUTTON)

    def fill_rental_info(self, date, rental_period, color, comment):
        self.input_text(self.DATE_INPUT, date)
        
        # Выбор периода аренды
        self.click_element(self.RENTAL_PERIOD_DROPDOWN)
        period_option = (By.XPATH, f"//div[contains(text(), '{rental_period}')]")
        self.click_element(period_option)
        
        # Выбор цвета
        if color == "black":
            self.click_element(self.COLOR_BLACK_CHECKBOX)
        elif color == "grey":
            self.click_element(self.COLOR_GREY_CHECKBOX)
        
        self.input_text(self.COMMENT_INPUT, comment)

    def click_order_button(self):
        self.click_element(self.ORDER_BUTTON)

    def confirm_order(self):
        self.click_element(self.CONFIRM_ORDER_BUTTON)

    def is_success_message_displayed(self):
        return self.is_element_visible(self.SUCCESS_MESSAGE)

    def get_success_message_text(self):
        return self.find_element(self.SUCCESS_MESSAGE).text

    def is_order_page_loaded(self):
        """Проверяет, что загружена страница заказа"""
        return self.get_current_url() == urls.ORDER_PAGE_URL