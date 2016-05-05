#!/usr/bin/env python

from unittest import TestCase, main

from selenium import webdriver


class SimpleVisitorTest(TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_home(self):
        self.browser.get('http://localhost:8000')
        self.assertTrue(self.browser.title.startswith('Caracole'))


if __name__ == '__main__':
    main()
