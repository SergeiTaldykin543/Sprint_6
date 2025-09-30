# order_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage
import urls


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

    def __init__(self, driver):
        super().__init__(driver)
        self.url = urls.ORDER_PAGE_URL

    def open(self):
        self.driver.get(self.url)
        self.wait_for_element_visible((By.CLASS_NAME, "Order_Header__BZXOb"))

    def check_for_validation_errors(self):
        error_elements = self.driver.find_elements(*self.ERROR_MESSAGES)
        visible_errors = []
        
        for error in error_elements:
            if error.is_displayed() and error.text.strip():
                visible_errors.append(error.text)
        
        return bool(visible_errors)

    def fill_personal_info(self, first_name, last_name, address, metro_station, phone):
        try:
            fields_to_fill = [
                (self.FIRST_NAME_INPUT, first_name),
                (self.LAST_NAME_INPUT, last_name),
                (self.ADDRESS_INPUT, address),
                (self.PHONE_INPUT, phone)
            ]
            
            for locator, value in fields_to_fill:
                field = self.wait.until(EC.element_to_be_clickable(locator))
                field.clear()
                field.send_keys(value)
                
                WebDriverWait(self.driver, 2).until(lambda driver: field.get_attribute('value') == value)
                
                if self.check_for_validation_errors():
                    return False
            
            metro_success = self.select_metro_station(metro_station)
            if not metro_success:
                return False
            
            if self.check_for_validation_errors():
                return False
                
            return True
            
        except Exception:
            return False

    def select_metro_station(self, station_name):
        try:
            metro_field = self.wait.until(EC.element_to_be_clickable(self.METRO_STATION_INPUT))
            metro_field.click()
            
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.METRO_DROPDOWN_OPTIONS))
            
            metro_field.send_keys(station_name)
            
            WebDriverWait(self.driver, 5).until(lambda driver: len(driver.find_elements(*self.METRO_DROPDOWN_OPTIONS)) > 0)
            
            station_options = self.driver.find_elements(*self.METRO_DROPDOWN_OPTIONS)
            station_found = False
            
            for option in station_options:
                if station_name in option.text:
                    button = option.find_element(*self.METRO_OPTION_BUTTON)
                    button.click()
                    station_found = True
                    break
            
            if not station_found and station_options:
                first_option = station_options[0]
                button = first_option.find_element(*self.METRO_OPTION_BUTTON)
                button.click()
                station_found = True
            
            if station_found:
                WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(self.METRO_DROPDOWN_OPTIONS))
                return True
            else:
                return False
                
        except Exception:
            return False

    def _is_first_page_visible(self):
        try:
            return WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT)).is_displayed()
        except:
            return False

    def _is_second_page_visible(self):
        try:
            second_page_elements = [
                self.RENTAL_HEADER,
                self.DATE_INPUT,
                self.RENTAL_PERIOD_DROPDOWN
            ]
            
            for element_locator in second_page_elements:
                try:
                    element = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(element_locator))
                    if element.is_displayed():
                        return True
                except:
                    continue
            
            return False
        except Exception:
            return False

    def click_next_button(self):
        try:
            if self.check_for_validation_errors():
                return False
            
            next_button = self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON))
            
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.NEXT_BUTTON))
            
            next_button.click()
            
            try:
                WebDriverWait(self.driver, 10).until(lambda driver: self._is_second_page_visible())
                return True
            except:
                return False
                
        except Exception:
            return False

    def close_calendar_if_visible(self):
        try:
            calendar = self.driver.find_elements(*self.CALENDAR)
            if calendar and calendar[0].is_displayed():
                date_field = self.driver.find_element(*self.DATE_INPUT)
                date_field.send_keys(Keys.ESCAPE)
                return True
        except Exception:
            pass
        return False

    def fill_rental_info(self, date, rental_period, color, comment):
        try:
            date_field = self.wait.until(EC.element_to_be_clickable(self.DATE_INPUT))
            date_field.clear()
            date_field.send_keys(date)
            
            WebDriverWait(self.driver, 5).until(lambda driver: date_field.get_attribute('value') == date)
            
            self.close_calendar_if_visible()
            
            self.select_rental_period(rental_period)
            
            if color == "black":
                color_checkbox = self.wait.until(EC.element_to_be_clickable(self.COLOR_BLACK_CHECKBOX))
                if not color_checkbox.is_selected():
                    color_checkbox.click()
            elif color == "grey":
                color_checkbox = self.wait.until(EC.element_to_be_clickable(self.COLOR_GREY_CHECKBOX))
                if not color_checkbox.is_selected():
                    color_checkbox.click()
            
            comment_field = self.wait.until(EC.element_to_be_clickable(self.COMMENT_INPUT))
            comment_field.clear()
            comment_field.send_keys(comment)
            
            WebDriverWait(self.driver, 5).until(lambda driver: comment_field.get_attribute('value') == comment)
            
        except Exception as e:
            raise

    def select_rental_period(self, rental_period):
        try:
            dropdown = self.wait.until(EC.element_to_be_clickable(self.RENTAL_PERIOD_DROPDOWN))
            
            self.driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
            
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.RENTAL_PERIOD_DROPDOWN))
            
            dropdown.click()
            
            options = WebDriverWait(self.driver, 5).until(EC.visibility_of_all_elements_located(self.RENTAL_PERIOD_OPTIONS))
            
            option_found = False
            for option in options:
                if rental_period in option.text:
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'Dropdown-option') and contains(text(), '{rental_period}')]")))
                    option.click()
                    option_found = True
                    break
            
            if not option_found and options:
                options[0].click()
                
        except Exception:
            pass

    def click_order_button(self):
        try:
            order_button_locators = [
                (By.XPATH, "//button[contains(text(), 'Заказать') and @class='Button_Button__ra12g Button_Middle__1CSJM']"),
                (By.XPATH, "//button[contains(text(), 'Заказать')]"),
                (By.CLASS_NAME, "Button_Middle__1CSJM")
            ]
            
            order_button = None
            for locator in order_button_locators:
                try:
                    order_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(locator))
                    if "Заказать" in order_button.text:
                        break
                    else:
                        order_button = None
                except:
                    continue
            
            if not order_button:
                raise Exception("Order button not found with any locator")
            
            self.driver.execute_script("arguments[0].scrollIntoView(true);", order_button)
            
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(order_button_locators[0]))
            
            order_button.click()
            
        except Exception as e:
            raise

    def confirm_order(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'Order_Modal')]")))
            
            confirm_button_locators = [
                (By.XPATH, "//button[contains(text(), 'Да')]"),
                (By.XPATH, "//div[contains(@class, 'Order_Modal')]//button[contains(text(), 'Да')]")]
            
            confirm_button = None
            for locator in confirm_button_locators:
                try:
                    confirm_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
                    break
                except:
                    continue
            
            if not confirm_button:
                raise Exception("Confirm button not found")
            
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(confirm_button_locators[0]))
            
            confirm_button.click()
            
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            
        except Exception as e:
            raise

    def is_success_message_displayed(self):
        try:
            return self.is_element_visible(self.SUCCESS_MESSAGE)
        except Exception:
            return False