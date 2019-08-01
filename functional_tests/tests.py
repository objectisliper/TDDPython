import unittest
import time
from functools import wraps

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from django.test import LiveServerTestCase


def wait_for_element_to_found(time_to_wait: int = 10):
    def inner_function(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    function(*args, **kwargs)
                    return
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > time_to_wait:
                        raise e
                    time.sleep(0.5)
        return wrapper
    return inner_function

class Browser(webdriver.Chrome):

    @wait_for_element_to_found()
    def find_element(self, by=By.ID, value=None):
        if self.w3c:
            if by == By.ID:
                by = By.CSS_SELECTOR
                value = '[id="%s"]' % value
            elif by == By.TAG_NAME:
                by = By.CSS_SELECTOR
            elif by == By.CLASS_NAME:
                by = By.CSS_SELECTOR
                value = ".%s" % value
            elif by == By.NAME:
                by = By.CSS_SELECTOR
                value = '[name="%s"]' % value
        return self.execute(Command.FIND_ELEMENT, {
            'using': by,
            'value': value})['value']


class NewVisitorTest(LiveServerTestCase):
    """ New user test """

    def setUp(self) -> None:
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        # User quit site

        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')

        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text, [row.text for row in rows])

    @wait_for_element_to_found()
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

        time.sleep(1)

        # Enter a name of point

        inputbox = self.browser.find_element_by_id('id_new_item')

        inputbox.send_keys('Buy smthng else')

        # Save changes

        inputbox.send_keys(Keys.ENTER)

        # check is saved

        self.wait_for_row_in_list_table('1: Buy smthng')

        self.wait_for_row_in_list_table('2: Buy smthng else')




if __name__ == '__main__':
    unittest.main(warnings='ignore')

