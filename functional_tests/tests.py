from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import unittest
import time
import os


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        test_server = os.environ.get('TEST_SERVER')
        if test_server:
            self.live_server_url = 'http://' + test_server
        # self.live_server_url = 'http://dietplanner-staging.kesug.com'



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
        edith_list_url = self.browser.current_url

        self.assertRegex(edith_list_url, '/lists/.+')
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

        # new user Franek visits page

        ## use new browser session to be sure that no previous information will be revealed eg by cookies
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Franek can't find any traces of previous list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Kupić pawie pióra', page_text)
        self.assertNotIn('zrobienia przynęty', page_text)

        # Franek creates new list by entering new element
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Kupić mleko')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        # Franek gets unique url adres to his list
        francis_list_url = self.browser.current_url

        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again there is no trace of previous list
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Kupić pawie pióra', page_text)
        self.assertIn('Kupić mleko', page_text)

    def test_layout_and_styling(self):
        # go to main page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # text field centered
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # new list page text field centered
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
