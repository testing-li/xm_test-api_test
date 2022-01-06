#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui.core.page.main.b_home import CompanyMain
from ui.core.page.official.account_login import AccountLogin
from ui.core.page.official.wv_login import VxLogin
from ui.core.page.basepage import BasePage
from selenium.webdriver.common.by import By


class CommonLogin(BasePage):
    def __init__(self, driver):
        BasePage.__init__(self, driver)
        self.common_button = (By.XPATH, '//*[@type="common"]')
        self.phone_input = (By.CSS_SELECTOR, '[placeholder="手机号"]')
        self.get_code = (By.CSS_SELECTOR, ".xm-input__checkcode-button")
        self.code_input = (By.CSS_SELECTOR, '[placeholder="验证码"]')


    def phone_login(self, phone, code, getcode=True, isTrue=True):
        self.find_element(self.common_button).click()
        self.find_element(self.phone_input).send_keys(phone)
        self.find_element(self.code_input).send_keys(code)
        if getcode:
            self.find_element(self.get_code).click()
        self.find_element(By.CSS_SELECTOR, "div:nth-child(1) button").click()
        if isTrue:
            return CompanyMain(self._driver)

    def phone_select_company(self, org_code=None, isAccpet=True):
        if not org_code:
            self.find_element((By.XPATH, f'//input[@value="{org_code}"]')).click()
        if isAccpet:
            self.find_element(By.CSS_SELECTOR,
                              "div:nth-child(15) button.el-button.el-button--primary.el-button--medium").click()
        else:
            self.find_element(By.CSS_SELECTOR,
                              "div:nth-child(15) button.el-button.el-button--default.el-button--medium").click()
        return CompanyMain(self._driver)

    def goto_account_login(self):
        self.find_element((By.XPATH,'//*[@type="account"]')).click()
        return AccountLogin(self._driver)

    def goto_wv_login(self):
        self.find_element(By.CSS_SELECTOR, '.wecaht-btn').click()
        return VxLogin(self._driver)

    def goto_home(self):
        from ui.core.page.official.home import Home
        self.find_element(By.CSS_SELECTOR, '.back-link.nuxt-link-active').click()
        return Home(self._driver)
