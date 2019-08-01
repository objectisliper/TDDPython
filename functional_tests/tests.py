import unittest
import time
from functools import wraps

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.by import By

from django.test import LiveServerTestCase


class ChromeWebdriver(webdriver.Chrome):

    time_to_wait = 10

    def find_element(self, by=By.ID, value=None):
        start_time = time.time()
        while True:
            try:
                return super().find_element(by, value)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.time_to_wait:
                    raise e
                time.sleep(0.5)


class NewVisitorTest(LiveServerTestCase):
    """ New user test """

    def setUp(self) -> None:
        self.browser = ChromeWebdriver()

    def tearDown(self) -> None:
        # User quit site

        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')

        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Юзер заходит на сайт

        self.browser.get(self.live_server_url)

        # Check title

        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text

        self.assertIn('To-Do', header_text)

        # Find input field

        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Enter a name of point

        inputbox.send_keys('Buy smthng')

        # Save changes

        inputbox.send_keys(Keys.ENTER)

        # Enter a name of point

        inputbox = self.browser.find_element_by_id('id_new_item')

        inputbox.send_keys('Buy smthng else')

        # Save changes

        inputbox.send_keys(Keys.ENTER)

        # check is saved

        self.wait_for_row_in_list_table('1: Buy smthng')

        self.wait_for_row_in_list_table('2: Buy smthng else')

        self.fail('looolz')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

