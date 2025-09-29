import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import os


@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания и закрытия драйвера"""
    
    # Вариант 1: Используем драйвер из PATH если он уже установлен
    try:
        # Пробуем создать драйвер без webdriver-manager
        service = Service()
        driver = webdriver.Firefox(service=service)
        print("✅ Firefox driver created using system PATH")
        
    except Exception as e:
        print(f"❌ Error creating driver from PATH: {e}")
        
        # Вариант 2: Ручная установка драйвера
        print("🔄 Trying alternative approach...")
        
        # Указываем путь к geckodriver вручную (если он уже скачан)
        geckodriver_path = "C:/WebDriver/geckodriver.exe"  # или другой путь
        
        if os.path.exists(geckodriver_path):
            service = Service(geckodriver_path)
            driver = webdriver.Firefox(service=service)
            print("✅ Firefox driver created using manual path")
        else:
            # Вариант 3: Используем Chrome как запасной вариант
            try:
                from selenium.webdriver.chrome.service import Service as ChromeService
                from webdriver_manager.chrome import ChromeDriverManager
                
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service)
                print("✅ Chrome driver created as fallback")
            except:
                raise Exception("Cannot create any WebDriver. Please install Firefox or Chrome driver manually.")
    
    driver.maximize_window()
    yield driver
    driver.quit()