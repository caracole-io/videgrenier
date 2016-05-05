#!/usr/bin/env python

from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')
assert browser.title.startswith('Caracole'), "Browser title was " + browser.title
