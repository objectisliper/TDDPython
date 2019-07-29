from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(unittest.TestCase):
    """ New user test """

    def setUp(self) -> None:
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        # User quit site

        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Юзер заходит на сайт

        self.browser.get('http://localhost:8000')

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

        # check is saved

        table = self.browser.find_element_by_id('id_list_table')

        rows = table.find_elements_by_tag_name('tr')

        self.assertTrue(
            any(row.text == 'Buy smthng' for row in rows),
            'Новый элемент списка не появился в таблице'
        )

        self.fail('Закончить тест!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

