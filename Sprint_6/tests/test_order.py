import pytest
import allure
from pages.main_page import MainPage
from pages.order_page import OrderPage
import data
import urls


@allure.feature('Order Flow')
class TestOrder:
    
    @allure.title('Test successful order - {order_data[dataset_name]} from {order_data[entry_point]}')
    @pytest.mark.parametrize('order_data', data.OrderData.ORDER_TEST_DATA)
    def test_successful_order(self, driver, order_data):
        with allure.step('Open main page'):
            main_page = MainPage(driver)
            main_page.open()
        
        with allure.step(f"Click order button from {order_data['entry_point']}"):
            if order_data['entry_point'] == 'top_button':
                main_page.click_order_button_top()
            else:
                main_page.click_order_button_bottom()
        
        with allure.step('Fill order form'):
            order_page = OrderPage(driver)
            self._fill_complete_order_form(order_page, order_data)
        
        with allure.step('Verify success message'):
            assert order_page.is_success_message_displayed(), \
                "Success message is not displayed after order confirmation"

    def _fill_complete_order_form(self, order_page, order_data):
        """Заполнение полной формы заказа"""
        # Первая страница - личная информация
        personal_info = order_data['personal_info']
        order_page.fill_personal_info(
            personal_info['first_name'],
            personal_info['last_name'],
            personal_info['address'],
            personal_info['metro_station'],
            personal_info['phone']
        )
        order_page.click_next_button()
        
        # Вторая страница - информация об аренде
        rental_info = order_data['rental_info']
        order_page.fill_rental_info(
            rental_info['date'],
            rental_info['rental_period'],
            rental_info['color'],
            rental_info['comment']
        )
        order_page.click_order_button()
        order_page.confirm_order()

    @allure.title('Test scooter logo redirect')
    def test_scooter_logo_redirect(self, driver):
        with allure.step('Open order page'):
            order_page = OrderPage(driver)
            order_page.open()
        
        with allure.step('Click scooter logo'):
            main_page = MainPage(driver)
            main_page.click_scooter_logo()
        
        with allure.step('Verify redirect to main page'):
            assert main_page.is_main_page_loaded(), \
                "Redirect to main page failed after clicking scooter logo"

    @allure.title('Test yandex logo redirect')
    def test_yandex_logo_redirect(self, driver):
        with allure.step('Open main page'):
            main_page = MainPage(driver)
            main_page.open()
        
        with allure.step('Click yandex logo'):
            main_window = driver.current_window_handle
            main_page.click_yandex_logo()
        
        with allure.step('Switch to new window and verify redirect'):
            all_windows = driver.window_handles
            new_window = [window for window in all_windows if window != main_window][0]
            driver.switch_to.window(new_window)
            
            driver.implicitly_wait(10)
            current_url = driver.current_url
            
            # Проверяем, что URL содержит ожидаемые домены
            redirect_success = any(domain in current_url for domain in urls.YANDEX_REDIRECT_URLS)
            assert redirect_success, \
                f"Redirect to Yandex/Dzen failed. Current URL: {current_url}"