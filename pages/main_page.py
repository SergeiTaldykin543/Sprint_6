# main_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import urls
import allure


class MainPage(BasePage):
    FAQ_QUESTIONS = {
        "Сколько это стоит? И как оплатить?": (By.ID, "accordion__heading-0"),
        "Хочу сразу несколько самокатов! Так можно?": (By.ID, "accordion__heading-1"),
        "Как рассчитывается время аренды?": (By.ID, "accordion__heading-2"),
        "Можно ли заказать самокат прямо на сегодня?": (By.ID, "accordion__heading-3"),
        "Можно ли продлить заказ или вернуть самокат раньше?": (By.ID, "accordion__heading-4"),
        "Вы привозите зарядку вместе с самокатом?": (By.ID, "accordion__heading-5"),
        "Можно ли отменить заказ?": (By.ID, "accordion__heading-6"),
        "Я жизу за МКАДом, привезёте?": (By.ID, "accordion__heading-7")
    }
    
    FAQ_ANSWERS = {
        "Сколько это стоит? И как оплатить?": (By.ID, "accordion__panel-0"),
        "Хочу сразу несколько самокатов! Так можно?": (By.ID, "accordion__panel-1"),
        "Как рассчитывается время аренды?": (By.ID, "accordion__panel-2"),
        "Можно ли заказать самокат прямо на сегодня?": (By.ID, "accordion__panel-3"),
        "Можно ли продлить заказ или вернуть самокат раньше?": (By.ID, "accordion__panel-4"),
        "Вы привозите зарядку вместе с самокатом?": (By.ID, "accordion__panel-5"),
        "Можно ли отменить заказ?": (By.ID, "accordion__panel-6"),
        "Я жизу за МКАДом, привезёте?": (By.ID, "accordion__panel-7")
    }

    ORDER_BUTTON_TOP = (By.XPATH, "//button[contains(text(), 'Заказать') and parent::div[@class='Header_Nav__AGCXC']]")
    ORDER_BUTTON_BOTTOM = (By.XPATH, "//button[contains(text(), 'Заказать') and parent::div[@class='Home_FinishButton__1_cWm']]")

    SCOOTER_LOGO = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
    YANDEX_LOGO = (By.CLASS_NAME, "Header_LogoYandex__3TSOI")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = urls.MAIN_PAGE_URL

    @allure.step("Открыть главную страницу")
    def open(self):
        self.driver.get(self.url)
        self.wait_for_element_visible((By.CLASS_NAME, "Home_Header__iJKdX"))

    @allure.step("Нажать на вопрос FAQ: '{question_text}'")
    def click_faq_question(self, question_text):
        question_locator = self.FAQ_QUESTIONS.get(question_text)
        if question_locator:
            self.scroll_to_element(question_locator)
            element = self.wait_for_element_clickable(question_locator)
            element.click()

    @allure.step("Получить текст ответа на вопрос: '{question_text}'")
    def get_faq_answer_text(self, question_text):
        answer_locator = self.FAQ_ANSWERS.get(question_text)
        if answer_locator:
            try:
                answer_element = self.wait_for_element_visible(answer_locator)
                return answer_element.text
            except:
                return None
        return None

    @allure.step("Проверить отображение ответа на вопрос: '{question_text}'")
    def is_faq_answer_displayed(self, question_text):
        answer_locator = self.FAQ_ANSWERS.get(question_text)
        return self.is_element_visible(answer_locator)

    @allure.step("Нажать верхнюю кнопку 'Заказать'")
    def click_order_button_top(self):
        """Клик по верхней кнопке Заказать с ожиданием открытия формы"""
        button = self.wait_for_element_clickable(self.ORDER_BUTTON_TOP)
        button.click()
        self._wait_for_order_form_opened()

    @allure.step("Нажать нижнюю кнопку 'Заказать'")
    def click_order_button_bottom(self):
        """Клик по нижней кнопке Заказать с ожиданием открытия формы"""
        # Прокручиваем к нижней кнопке
        self.scroll_to_element(self.ORDER_BUTTON_BOTTOM)
        
        # Ждем пока кнопка станет кликабельной
        button = self.wait_for_element_clickable(self.ORDER_BUTTON_BOTTOM)
        
        # Кликаем и ждем открытия формы заказа
        button.click()
        self._wait_for_order_form_opened()

    def _wait_for_order_form_opened(self):
        """Ожидание открытия формы заказа"""
        # Ждем появления заголовка формы заказа
        try:
            self.wait.until(EC.url_contains("/order"))
        except:
            # Если URL не изменился, проверяем наличие элементов формы заказа
            order_form_indicators = [
                (By.CLASS_NAME, "Order_Header__BZXOb"),
                (By.XPATH, "//input[@placeholder='* Имя']"),
                (By.XPATH, "//input[@placeholder='* Фамилия']")
            ]
            
            for indicator in order_form_indicators:
                try:
                    self.wait_for_element_visible(indicator, timeout=10)
                    return
                except:
                    continue
            
            # Если форма не открылась, пробуем обновить страницу и повторить
            self.driver.refresh()
            self.wait_for_element_visible((By.CLASS_NAME, "Order_Header__BZXOb"), timeout=10)

    @allure.step("Нажать логотип Самоката")
    def click_scooter_logo(self):
        self.click_element(self.SCOOTER_LOGO)

    @allure.step("Нажать логотип Яндекса")
    def click_yandex_logo(self):
        self.click_element(self.YANDEX_LOGO)

    @allure.step("Проверить загрузку главной страницы")
    def is_main_page_loaded(self):
        return self.driver.current_url == urls.MAIN_PAGE_URL

    @allure.step("Проверить успешность редиректа на Яндекс")
    def is_yandex_redirect_successful(self):
        return self.switch_to_new_window_and_verify_redirect(urls.YANDEX_REDIRECT_URLS)