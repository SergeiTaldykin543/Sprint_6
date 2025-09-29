from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import urls


class OrderPage(BasePage):
    # Локаторы формы заказа - первая страница
    FIRST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Имя']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_STATION_INPUT = (By.XPATH, "//input[@placeholder='* Станция метро']")
    PHONE_INPUT = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.CLASS_NAME, "Button_Middle__1CSJM")

    # Локаторы для ошибок валидации
    ERROR_MESSAGES = (By.CLASS_NAME, "Input_ErrorMessage__3HvIb")

    # Локаторы второй страницы
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

    # Локаторы для выпадающего списка метро
    METRO_DROPDOWN_OPTIONS = (By.CLASS_NAME, "select-search__row")
    METRO_OPTION_BUTTON = (By.XPATH, ".//button")

    # Локаторы для календаря
    CALENDAR = (By.CLASS_NAME, "react-datepicker")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = urls.ORDER_PAGE_URL

    def open(self):
        self.driver.get(self.url)
        self.wait_for_element_visible((By.CLASS_NAME, "Order_Header__BZXOb"))

    def check_for_validation_errors(self):
        """Проверяет наличие ошибок валидации"""
        error_elements = self.driver.find_elements(*self.ERROR_MESSAGES)
        visible_errors = []
        
        for error in error_elements:
            # Проверяем что ошибка видима и имеет текст
            if error.is_displayed() and error.text.strip():
                visible_errors.append(error.text)
        
        if visible_errors:
            print(f"❌ Validation errors found: {visible_errors}")
            return True
        return False

    def fill_personal_info(self, first_name, last_name, address, metro_station, phone):
        print(f"📝 Filling personal info: {first_name} {last_name}")
        
        try:
            # Заполняем поля по очереди
            fields_to_fill = [
                (self.FIRST_NAME_INPUT, first_name, "First name"),
                (self.LAST_NAME_INPUT, last_name, "Last name"),
                (self.ADDRESS_INPUT, address, "Address"),
                (self.PHONE_INPUT, phone, "Phone")
            ]
            
            for locator, value, field_name in fields_to_fill:
                field = self.wait.until(EC.element_to_be_clickable(locator))
                field.clear()
                field.send_keys(value)
                print(f"  ✅ {field_name}: {value}")
                
                # Ждем обновления состояния формы
                WebDriverWait(self.driver, 2).until(
                    lambda driver: field.get_attribute('value') == value
                )
                
                # Проверяем ошибки после каждого поля
                if self.check_for_validation_errors():
                    print(f"❌ Validation error after filling {field_name}")
                    return False
            
            # Выбор станции метро
            print(f"🚇 Selecting metro station: {metro_station}")
            metro_success = self.select_metro_station(metro_station)
            if not metro_success:
                print("❌ Failed to select metro station")
                return False
            
            # Финальная проверка ошибок
            if self.check_for_validation_errors():
                print("❌ Validation errors after filling all fields")
                return False
                
            print("✅ All personal info filled successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error filling personal info: {e}")
            return False

    def select_metro_station(self, station_name):
        print(f"🚇 Selecting metro station: {station_name}")
        
        try:
            # Кликаем на поле выбора метро
            metro_field = self.wait.until(EC.element_to_be_clickable(self.METRO_STATION_INPUT))
            metro_field.click()
            
            # Ждем появления выпадающего списка
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.METRO_DROPDOWN_OPTIONS)
            )
            
            # Вводим название станции
            metro_field.send_keys(station_name)
            
            # Ждем обновления списка станций
            WebDriverWait(self.driver, 5).until(
                lambda driver: len(driver.find_elements(*self.METRO_DROPDOWN_OPTIONS)) > 0
            )
            
            # Ищем станцию в выпадающем списке
            station_options = self.driver.find_elements(*self.METRO_DROPDOWN_OPTIONS)
            station_found = False
            
            for option in station_options:
                if station_name in option.text:
                    # Нажимаем кнопку внутри элемента option
                    button = option.find_element(*self.METRO_OPTION_BUTTON)
                    button.click()
                    print(f"✅ Metro station selected: {station_name}")
                    station_found = True
                    break
            
            if not station_found and station_options:
                # Если точного совпадения нет, выбираем первую станцию
                first_option = station_options[0]
                button = first_option.find_element(*self.METRO_OPTION_BUTTON)
                button.click()
                print(f"✅ Selected first available station: {first_option.text}")
                station_found = True
            
            if station_found:
                # Ждем скрытия выпадающего списка
                WebDriverWait(self.driver, 5).until(
                    EC.invisibility_of_element_located(self.METRO_DROPDOWN_OPTIONS)
                )
                return True
            else:
                print("❌ No metro stations found in dropdown")
                return False
                
        except Exception as e:
            print(f"❌ Error selecting metro station: {e}")
            return False

    def _is_first_page_visible(self):
        """Проверяет, видима ли первая страница формы заказа"""
        try:
            return WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self.FIRST_NAME_INPUT)
            ).is_displayed()
        except:
            return False

    def _is_second_page_visible(self):
        """Проверяет, видима ли вторая страница формы заказа"""
        try:
            # Проверяем несколько элементов второй страницы
            second_page_elements = [
                self.RENTAL_HEADER,
                self.DATE_INPUT,
                self.RENTAL_PERIOD_DROPDOWN
            ]
            
            for element_locator in second_page_elements:
                try:
                    element = WebDriverWait(self.driver, 5).until(
                        EC.visibility_of_element_located(element_locator)
                    )
                    if element.is_displayed():
                        print(f"✅ Second page element found: {element_locator}")
                        return True
                except:
                    continue
            
            print("❌ No second page elements found")
            return False
        except Exception as e:
            print(f"❌ Error checking second page: {e}")
            return False

    def click_next_button(self):
        print("➡️ Clicking next button")
        
        try:
            # Проверяем ошибки перед нажатием
            if self.check_for_validation_errors():
                print("❌ Cannot proceed - validation errors present")
                return False
            
            # Находим кнопку
            next_button = self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON))
            
            # Прокручиваем к элементу
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            
            # Ждем пока элемент станет полностью кликабельным
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.NEXT_BUTTON)
            )
            
            # Кликаем кнопку
            next_button.click()
            
            # Ждем перехода на вторую страницу
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: self._is_second_page_visible()
                )
                print("✅ Successfully moved to second page")
                return True
            except:
                print("❌ Failed to move to second page")
                return False
                
        except Exception as e:
            print(f"❌ Error clicking next button: {e}")
            return False

    def close_calendar_if_visible(self):
        """Закрывает календарь даты, если он открыт и мешает"""
        try:
            # Проверяем, открыт ли календарь
            calendar = self.driver.find_elements(*self.CALENDAR)
            if calendar and calendar[0].is_displayed():
                print("📅 Calendar is open, closing it...")
                # Нажимаем Escape для закрытия календаря
                from selenium.webdriver.common.keys import Keys
                date_field = self.driver.find_element(*self.DATE_INPUT)
                date_field.send_keys(Keys.ESCAPE)
                print("✅ Calendar closed with Escape key")
                return True
        except Exception as e:
            print(f"⚠️ Could not close calendar: {e}")
        return False

    def fill_rental_info(self, date, rental_period, color, comment):
        print(f"📅 Filling rental info: {date}, {rental_period}, {color}")
        
        try:
            # Заполняем дату
            date_field = self.wait.until(EC.element_to_be_clickable(self.DATE_INPUT))
            date_field.clear()
            date_field.send_keys(date)
            
            # Ждем заполнения даты
            WebDriverWait(self.driver, 5).until(
                lambda driver: date_field.get_attribute('value') == date
            )
            print(f"✅ Date filled: {date}")
            
            # Закрываем календарь если он открылся
            self.close_calendar_if_visible()
            
            # Выбираем период аренды
            self.select_rental_period(rental_period)
            
            # Выбираем цвет
            if color == "black":
                color_checkbox = self.wait.until(EC.element_to_be_clickable(self.COLOR_BLACK_CHECKBOX))
                if not color_checkbox.is_selected():
                    color_checkbox.click()
                print("✅ Color selected: black")
            elif color == "grey":
                color_checkbox = self.wait.until(EC.element_to_be_clickable(self.COLOR_GREY_CHECKBOX))
                if not color_checkbox.is_selected():
                    color_checkbox.click()
                print("✅ Color selected: grey")
            
            # Заполняем комментарий
            comment_field = self.wait.until(EC.element_to_be_clickable(self.COMMENT_INPUT))
            comment_field.clear()
            comment_field.send_keys(comment)
            
            # Ждем заполнения комментария
            WebDriverWait(self.driver, 5).until(
                lambda driver: comment_field.get_attribute('value') == comment
            )
            print(f"✅ Comment filled: {comment}")
            
            print("✅ All rental info filled successfully")
            
        except Exception as e:
            print(f"❌ Error filling rental info: {e}")
            raise

    def select_rental_period(self, rental_period):
        print(f"⏱️ Selecting rental period: {rental_period}")
        
        try:
            # Находим выпадающий список
            dropdown = self.wait.until(EC.element_to_be_clickable(self.RENTAL_PERIOD_DROPDOWN))
            
            # Прокручиваем к элементу
            self.driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
            
            # Ждем пока элемент станет кликабельным
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.RENTAL_PERIOD_DROPDOWN)
            )
            
            # Кликаем на выпадающий список
            dropdown.click()
            
            # Ждем появления опций
            options = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_all_elements_located(self.RENTAL_PERIOD_OPTIONS)
            )
            print(f"Found {len(options)} rental period options")
            
            option_found = False
            for option in options:
                if rental_period in option.text:
                    print(f"🎯 Selecting: {option.text}")
                    # Ждем пока опция станет кликабельной
                    WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'Dropdown-option') and contains(text(), '{rental_period}')]"))
                    )
                    option.click()
                    print(f"✅ Rental period selected: {rental_period}")
                    option_found = True
                    break
            
            if not option_found and options:
                print(f"🔄 No exact match, selecting first option: {options[0].text}")
                options[0].click()
                print("✅ Selected first available option")
            elif not options:
                print("❌ No rental period options found")
                
        except Exception as e:
            print(f"❌ Error selecting rental period: {e}")

    def click_order_button(self):
        print("🛒 Clicking order button")
        
        try:
            # Ищем кнопку заказа с разными локаторами
            order_button_locators = [
                (By.XPATH, "//button[contains(text(), 'Заказать') and @class='Button_Button__ra12g Button_Middle__1CSJM']"),
                (By.XPATH, "//button[contains(text(), 'Заказать')]"),
                (By.CLASS_NAME, "Button_Middle__1CSJM")
            ]
            
            order_button = None
            for locator in order_button_locators:
                try:
                    order_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable(locator)
                    )
                    # Проверяем что это кнопка заказа по тексту
                    if "Заказать" in order_button.text:
                        print(f"✅ Found order button with locator: {locator}")
                        break
                    else:
                        order_button = None
                except:
                    continue
            
            if not order_button:
                raise Exception("Order button not found with any locator")
            
            # Прокручиваем к элементу
            self.driver.execute_script("arguments[0].scrollIntoView(true);", order_button)
            
            # Ждем пока кнопка станет полностью кликабельной
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(order_button_locators[0])
            )
            
            # Кликаем кнопку заказа
            order_button.click()
            
            print("✅ Order button clicked")
            
        except Exception as e:
            print(f"❌ Error clicking order button: {e}")
            raise

    def confirm_order(self):
        print("✅ Confirming order")
        
        try:
            # Ждем появления модального окна подтверждения
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'Order_Modal')]"))
            )
            print("✅ Confirmation modal appeared")
            
            # Ищем кнопку подтверждения
            confirm_button_locators = [
                (By.XPATH, "//button[contains(text(), 'Да')]"),
                (By.XPATH, "//div[contains(@class, 'Order_Modal')]//button[contains(text(), 'Да')]")
            ]
            
            confirm_button = None
            for locator in confirm_button_locators:
                try:
                    confirm_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(locator)
                    )
                    print(f"✅ Found confirm button with locator: {locator}")
                    break
                except:
                    continue
            
            if not confirm_button:
                raise Exception("Confirm button not found")
            
            # Ждем пока кнопка станет полностью кликабельной
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(confirm_button_locators[0])
            )
            
            # Кликаем кнопку подтверждения
            confirm_button.click()
            
            print("✅ Order confirmed")
            
            # Ждем появления сообщения об успехе
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
            )
            print("✅ Success message appeared")
            
        except Exception as e:
            print(f"❌ Error confirming order: {e}")
            raise

    def is_success_message_displayed(self):
        try:
            is_displayed = self.is_element_visible(self.SUCCESS_MESSAGE)
            if is_displayed:
                message_element = self.driver.find_element(*self.SUCCESS_MESSAGE)
                message_text = message_element.text
                print(f"📋 Success message displayed: {message_text}")
            else:
                print("❌ Success message not displayed")
            return is_displayed
        except Exception as e:
            print(f"❌ Error checking success message: {e}")
            return False