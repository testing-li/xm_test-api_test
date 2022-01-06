# -*- coding: utf-8 -*-
from ui.core.page.official.common_login import CommonLogin
from ui.core.page.official.wv_login import VxLogin
from ui.core.page.basepage import BasePage
from selenium.webdriver.common.by import By


class Home(BasePage):
	_url = 'https://www.bestcem.com/'
	login_btn = (By.CSS_SELECTOR, ".login-btn.action-btn")
	wv_btn = (By.CSS_SELECTOR, ".login-wechat-btn.action-btn")

	def goto_phone_login(self):
		s = self.find_element(self.login_btn)
		s.click()
		return CommonLogin(self._driver)

	def goto_wv(self):
		self.find_element(self.wv_btn).click()
		return VxLogin(self._driver)
