from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import unittest
import time


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')

        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_app_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)

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
        self.check_for_row_in_list_table('1: Kupić pawie pióra')

        # There is text field prompting to enter another task to do on the website
        # enter: Użyć pawich piór do zrobienia przynęty
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Użyć pawich piór do zrobienia przynęty')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # page was uploaded and displays 2 elements on to do list
        self.check_for_row_in_list_table('1: Kupić pawie pióra')
        self.check_for_row_in_list_table('2: Użyć pawich piór do zrobienia przynęty')

        self.fail('End of test')
