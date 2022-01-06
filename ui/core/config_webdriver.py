# -*- coding: utf-8 -*-

from selenium import webdriver
import os

driver = None


def init_driver():
    browser = os.getenv('browser')
    global driver
    if not driver:
        if browser == '' or 'chrome':
            driver = webdriver.Chrome()
        elif browser == 'ie':
            driver = webdriver.Ie()
        elif browser == 'firefox':
            driver = webdriver.Firefox()
        else:
            pass
    return driver
