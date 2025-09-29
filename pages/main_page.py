from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import urls


class MainPage(BasePage):
    # Локаторы для FAQ
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

    # Локаторы для кнопок заказа
    ORDER_BUTTON_TOP = (By.XPATH, "//button[contains(text(), 'Заказать') and parent::div[@class='Header_Nav__AGCXC']]")
    ORDER_BUTTON_BOTTOM = (By.XPATH, "//button[contains(text(), 'Заказать') and parent::div[@class='Home_FinishButton__1_cWm']]")

    # Локаторы для логотипов
    SCOOTER_LOGO = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
    YANDEX_LOGO = (By.CLASS_NAME, "Header_LogoYandex__3TSOI")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = urls.MAIN_PAGE_URL

    def open(self):
        self.driver.get(self.url)
        # Ждем загрузки главного заголовка вместо полной загрузки страницы
        self.wait_for_element_visible((By.CLASS_NAME, "Home_Header__iJKdX"))

    def click_faq_question(self, question_text):
        question_locator = self.FAQ_QUESTIONS.get(question_text)
        if question_locator:
            print(f"🖱️  Clicking FAQ question: {question_text}")
            
            # Прокручиваем к элементу
            self.scroll_to_element(question_locator)
            
            # Ждем пока элемент станет кликабельным и кликаем через JavaScript
            element = self.wait_for_element_clickable(question_locator)
            self.driver.execute_script("arguments[0].click();", element)
            print("✅ Question clicked via JavaScript")

    def get_faq_answer_text(self, question_text):
        answer_locator = self.FAQ_ANSWERS.get(question_text)
        if answer_locator:
            try:
                answer_element = self.wait_for_element_visible(answer_locator)
                return answer_element.text
            except:
                return None
        return None

    def is_faq_answer_displayed(self, question_text):
        answer_locator = self.FAQ_ANSWERS.get(question_text)
        return self.is_element_visible(answer_locator)

    def click_order_button_top(self):
        self.click_element(self.ORDER_BUTTON_TOP)

    def click_order_button_bottom(self):
        self.click_element(self.ORDER_BUTTON_BOTTOM)

    def click_scooter_logo(self):
        self.click_element(self.SCOOTER_LOGO)

    def click_yandex_logo(self):
        self.click_element(self.YANDEX_LOGO)

    def is_main_page_loaded(self):
        return self.driver.current_url == urls.MAIN_PAGE_URL