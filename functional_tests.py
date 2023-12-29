from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import unittest
import time


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_app_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        # web title and header contain word "List"
        self.assertIn('List', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('List', header_text)

        # correct input of things to do
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 'Wpisz rzecz do zrobienia'
        )
        # enter "Kupić pawie pióra" in text field
        inputbox.send_keys('Kupić pawie pióra')

        # press enter key, website displays
        # "1: Kupić pawie pióra" as to do list element
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('1: Kupić pawie pióra', [row.text for row in rows])

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Użyć pawich piór do zrobienia przynęty')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('1: Kupić pawie pióra', [row.text for row in rows])
        self.assertIn('2: Użyć pawich piór do zrobienia przynęty', [row.text for row in rows])

        self.fail('End of test')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
