#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import allure
from api.core.bestcem import user
from api.utils.read_yaml import read_yaml


@allure.feature('authorize')
@allure.severity(allure.severity_level.BLOCKER)
class TestAuthorize:
    apis = user.Authorize()
    users = user.User()

    @allure.title('company login and get user info')
    @pytest.mark.parametrize(('org_code', 'username', 'password'),
                             read_yaml('/data/account_login.yml')['success']
                             )
    def test_company_login(self, org_code, username, password):
        with allure.step('通过公司域名登陆'):
            result1 = self.apis.post_company_token(org_code, username, password).json()
            assert result1['code'] == 0
            token = f"Bearer {result1['data']['token']}"
        with allure.step('获取公司信息'):
            result2 = self.users.get_company(token)
            assert result2.json()['code'] == 0
            assert result2.json()['data']['code'] in result2.url
        with allure.step('获取个人信息'):
            result3 = self.users.get_self(token)
            assert result3.json()['code'] == 0
            assert username in result3.text

    @allure.title('company login fail')
    @pytest.mark.parametrize(('org_code', 'username', 'password', 'error_code'),
                             read_yaml('/data/account_login.yml')['fail']
                             )
    def test_company_login_fail(self, org_code, username, password, error_code):
        result = self.apis.post_company_token(org_code, username, password).json()
        assert result['code'] == error_code


if __name__ == '__main__':
    pytest.main('./tests/')
# 执行用例
# pytest -q -s tests/test_user/ --clean-alluredir --alluredir=report/report_json/
# 生成报告
#  allure serve report/report_json/
