from selenium import webdriver
import unittest


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

        self.fail('Закончить тест!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

