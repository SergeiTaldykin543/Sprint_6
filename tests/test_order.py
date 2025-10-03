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

        with allure.step('Wait for order form to load'):
            order_page = OrderPage(driver)
            order_page.wait_for_order_form_loaded()

        with allure.step('Fill order form'):
            order_page.fill_complete_order_form(order_data)

        with allure.step('Verify success message'):
            assert order_page.is_success_message_displayed(), \
                "Success message is not displayed after order confirmation"

    @allure.title('Test scooter logo redirect')
    def test_scooter_logo_redirect(self, driver):
        with allure.step('Open order page'):
            order_page = OrderPage(driver)
            order_page.open()
        
        with allure.step('Click scooter logo'):
            order_page.click_scooter_logo()
        
        with allure.step('Verify redirect to main page'):
            main_page = MainPage(driver)
            assert main_page.is_main_page_loaded(), \
                "Failed to redirect to main page after clicking scooter logo"

    @allure.title('Test yandex logo redirect')
    def test_yandex_logo_redirect(self, driver):
        with allure.step('Open main page'):
            main_page = MainPage(driver)
            main_page.open()

        with allure.step('Click yandex logo'):
            main_page.click_yandex_logo()
        
        with allure.step('Switch to new window and verify redirect'):
            assert main_page.is_yandex_redirect_successful(), \
                "Redirect to Yandex/Dzen failed"