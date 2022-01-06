#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ui.core.page.official.home import Home
from _pytest import runner


class TestCase():
    def setup(self):
        self.home = Home()

    def teardown(self):
        self.home._driver.quit()

    def test_accountlogin(self):
        self.home.goto_phone_login().goto_account_login().account_login('123', '123')
        assert 1 == 2
