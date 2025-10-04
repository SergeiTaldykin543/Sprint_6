import pytest
import allure
from pages.main_page import MainPage
import data


@allure.feature('FAQ Section')
class TestFAQ:
    
    @allure.title('Test FAQ questions')
    @pytest.mark.parametrize('question_data', data.FAQData.QUESTIONS_AND_ANSWERS)
    def test_faq_question_answer(self, driver, question_data):
        with allure.step('Open main page'):
            main_page = MainPage(driver)
            main_page.open()
        
        with allure.step(f"Click on question: {question_data['question']}"):
            main_page.click_faq_question(question_data['question'])
        
        with allure.step('Verify answer is displayed'):
            assert main_page.is_faq_answer_displayed(question_data['question']), \
                f"Answer for '{question_data['question']}' is not displayed"
        
        with allure.step('Verify answer text'):
            actual_answer = main_page.get_faq_answer_text(question_data['question'])
            expected_answer = question_data['expected_answer']
            assert actual_answer == expected_answer, \
                f"Expected: {expected_answer}, Got: {actual_answer}"