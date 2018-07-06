import os

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Search(unittest.TestCase):
    def setUp(self):
        # Указываем где лежит веб-драйвер
        self.driver = webdriver.Chrome(executable_path='{}/webdrivers/chromedriver'.format(os.getcwd()))
        self.driver.implicitly_wait(8)
        self.driver.maximize_window()

    def tearDown(self):
        # Закрываем браузер
        self.driver.close()

    def test(self):
        # Step 1 Открыть страницу http://yandex.ru
        self.driver.get('https://www.google.ru/')
        assert 'Google' in self.driver.title

        # Step 2 Выполнить поиск слова “selenide”
        el = self.driver.find_element(By.XPATH, './/input[@title="Поиск"]')
        el.send_keys('selenide')
        el.send_keys(Keys.RETURN)

        # Step 3 Проверить, что первый результат – ссылка на сайт selenide.org.
        first_result_el = self.driver.find_element(By.XPATH, ".//div[@class='s']/descendant::cite")
        assert first_result_el.text == 'ru.selenide.org/'

        # Step 4 Перейти в раздел поиска изображений
        self.driver.find_element(By.XPATH, './/a[text()="Картинки"]').click()

        # Step 5 Проверить, что первое изображение неким образом связано с сайтом selenide.org
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
            (By.XPATH, ".//img[@alt='Картинки по запросу selenide']"))).click()
        first_pic_el = self.driver.find_element(By.XPATH, "(.//span[@class='irc_ho'])[2]")
        assert first_pic_el.text == 'ru.selenide.org'
        self.driver.find_element(By.XPATH, './/a[@aria-label="Закрыть"]').click()
        # Step 6 Вернуться в раздел поиска
        self.driver.find_element(By.XPATH, './/a[text()="Все"]').click()
        # Step 7 Проверить, что первый результат такой же, как и на шаге 3.
        first_result_el = self.driver.find_element(By.XPATH, './/div[@class="s"]/descendant::cite')
        assert first_result_el.text == 'ru.selenide.org/'

if __name__ == '__main__':
    unittest.main()
