# -*- coding: utf-8 -*-

from ui.core.page.basepage import BasePage
from selenium.webdriver.common.by import By


class AccountLogin(BasePage):
    def __init__(self, _url):

    def qdes_title(self, ):
        title = self.find_element((By.CSS_SELECTOR, '.q-begin__title'))
        return title

    # self.screen_shot('test')
    # self.find_element(By.CSS_SELECTOR, "div:nth-child(3) button").click()

    # return CompanyMain(self._driver)

    def account_select_company(self, org_code=None, isAccpet=True):
        if not org_code:
            self.find_element(locator=f'//input[@value="{org_code}"]').click()
        if isAccpet:
            self.find_element(By.CSS_SELECTOR,
                              "div:nth-child(15) button.el-button.el-button--primary.el-button--medium").click()
        else:
            self.find_element(By.CSS_SELECTOR,
                              "div:nth-child(15) button.el-button.el-button--default.el-button--medium").click()
        return CompanyMain(self._driver)

    def goto_forgetpassword(self):
        self.find_element(By.CSS_SELECTOR, ".password-link")
        return ForgetPassword(self._driver)

    def goto_register(self):
        self.find_element(By.CSS_SELECTOR, '.register-btn').click()
        return Register(self._driver)

    def goto_wv_login(self):
        self.find_element(By.CSS_SELECTOR, '.wecaht-btn').click()
        return VxLogin(self._driver)

    def goto_home(self):
        from ui.core.page.official.home import Home
        self.find_element(By.CSS_SELECTOR, '.back-link.nuxt-link-active').click()
        return Home(self._driver)
