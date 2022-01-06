# -*- coding: utf-8 -*-
import os
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from ui.core.utils.getdir import PROPATH
from ui.core import config_webdriver


class BasePage:
    def __init__(self, _url, driver: WebDriver = None):
        self._driver = None
        self._url = ''
        if not driver:
            self._driver = config_webdriver.init_driver()
        else:
            self._driver = driver
        if self._url != '':
            self._driver.get(self._url)
        self.option = Options()
        self.option.add_argument('disable-infobars')
        self._driver.implicitly_wait(3)
        self._driver.maximize_window()

    # 截图
    def screen_shot(self, name=''):
        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        picture_time = time.strftime("%H:%M:%S", time.localtime(time.time()))
        DatePath = f'{PROPATH}/report/screenshot/{date}/'
        if not os.path.exists(DatePath):
            os.mkdir(DatePath)
        # create a folder --- Automation_ScreenShot in the dir
        PictruePath = f'{DatePath}/{name}_{picture_time}.png'
        self._driver.save_screenshot(PictruePath)
        return PictruePath

    def find_element(self, locator=(), name=''):
        element = ''
        try:
            element = WebDriverWait(self._driver, 5).until(ec.presence_of_element_located((locator[0], locator[1])))
        except TimeoutException as e:
            pass
            # self.screen_shot(name)
            # there need to write log
        return element

    def find_elemens(self, locator=(), name=''):
        elements = ''
        try:
            elements = WebDriverWait(self._driver, 5).until(ec.presence_of_element_located((locator[0], locator[1])))
        except TimeoutException as e:
            if name == "":
                pass
            else:
                pass
        return elements
