#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import allure
from api.core.open_platform import open_organization
from api.utils import method


# @pytest.mark.skip(reason="租户创建")
@allure.feature('open_organization')
@allure.severity(allure.severity_level.NORMAL)
class TestOpenOraganization:
    instance_id = method.strNum(6)
    open_account = open_organization.OpenPlatformOrganization()

    # 创建租户
    @allure.title('连续创建租户')
    @pytest.mark.skip(reason="连续创建租户")
    @pytest.mark.parametrize(('code', 'name', "mobile", "email", "expire_dt", "instance_id"),
                             [
                                 ("", "众言科技", "17839236545", "", "", f"autoOpen{instance_id}")
                             ])
    def test_post_open_creat_account_once(self, code, name, mobile, email, expire_dt, instance_id):
        with allure.step("新建企业"):
            count = self.open_account.post_open_creat_account(code, name, mobile, email, expire_dt, instance_id)
            assert count['code'] == 0
        with allure.step("重复创建"):
            result = self.open_account.post_open_creat_account(code, name, mobile, email, expire_dt, instance_id)
            assert result.json()['code'] != 0

    @allure.title('创建租户')
    # @pytest.mark.skip(reason="租户创建")
    @pytest.mark.parametrize(('code', 'name', "mobile", "email", "expire_dt", "instance_id", "package"),
                             [
                                 ("opentestpackagezx1121", "众言科技", "", "xx.zong@idiaoyan.com", "2021/5/12",
                                  "opentestpackagezx1211", "高级版")
                                 # ("", "", None, "xx.zong@idiaoyan.com", "", f"autoOpen{method.strNum(5)}"),
                                 # (None, None, None, "xx.zong@idiaoyan.com", "", f"autoOpen{method.strNum(5)}"),
                                 # (None, "众言科技", "17839236545", "xx.zong@idiaoyan.com", "2021/3/28",
                                 #  f"autoOpen{method.strNum(5)}"),
                                 # (f"codeOpen{method.strNum(5)}", "众言科技", None, "xx.zong@idiaoyan.com",
                                 #  "2022/01/01", f"autoOpen{method.strNum(5)}"),
                                 # (f"codeOpen{method.strNum(5)}", "众言科技", "17839236545", "xx.zong@idiaoyan.com",
                                 #  "2022/01/01", f"autoOpen{method.strNum(5)}"),
                             ])
    def test_post_open_creat_account(self, code, name, mobile, email, expire_dt, instance_id, package):
        result = self.open_account.post_open_creat_account(code, name, mobile, email, expire_dt, instance_id,
                                                           package=package)
        assert result['code'] == 0
        if code:
            assert result['data']['code'] == code
        else:
            assert result['data'].get('code') is not None
        assert result['data']['mobile'] == mobile
        assert result['data']['email'] == email
        assert result['data']['instance_id'] == instance_id
        assert result['data'].get("secret_key") is not None
        assert result['data'].get("aes_key") is not None

    @allure.title('错误创建租户')
    @pytest.mark.parametrize(('code', 'name', "mobile", "email", "expire_dt", "instance_id"),
                             [
                                 (None, None, None, None, None, f"autoOpen{method.strNum(5)}"),
                                 (None, None, "17839236545", None, None, f"autoOpen{method.strNum(5)}"),
                                 ("autoOpen", "", "17839236545", "", "", f"autoOpen{method.strNum(5)}"),
                                 ("中文", "", "", "", "", "autoOpen"),
                                 ("@#￥%", "", "", "", "", ""),
                                 ("q_q-4", "", "", "", "", " "),
                                 (1, "", "", "", "", f"autoOpen{method.strNum(5)}"),
                                 ("", "", "1", "", "", f"autoOpen{method.strNum(5)}"),
                                 ("", "", "", "1", "", f"autoOpen{method.strNum(5)}"),
                                 ("", "", "", "", "1", f"autoOpen{method.strNum(5)}"),
                                 ("", "", "", "", "", 1),
                             ])
    def test_post_open_creat_account_fail(self, code, name, mobile, email, expire_dt, instance_id):
        result = self.open_account.post_open_creat_account(code, name, mobile, email, expire_dt, instance_id)
        if isinstance(result, dict):
            assert result['code'] != 0
            assert result['code'] != -1
        else:
            assert result.json()['code'] != 0
            assert result.json()['code'] != -1

    # 修改租户信息
    @allure.title('租户信息变更')
    @pytest.mark.parametrize(("mobile", "email", "expire_dt", "instance_id"),
                             [
                                 ("17839236545", "xx.zong@idiaoyan.com", "2022/01/01", "autoOpen"),  # 原数据更新
                                 # ("15400000001", "xx.zong@idiaoyan.com", "2022/01/01", "autoOpen"),  # 更新手机号
                                 # ("15400000001", "zongxiuxuan001@163.com", "2022/01/01", "autoOpen"),  # 更新邮箱
                                 # ("15400000001", "zongxiuxuan001@163.com", "2023/01/01", "autoOpen"),  # 更新日期
                                 # ("15400000001", "", "2023/01/01", "autoOpen"),  # 邮箱为空
                                 # ("15400000001", "xx.zong@idiaoyan.com", "", "autoOpen"),  # 日期为空
                                 # ("15400000001", "", "", "autoOpen"),  # 邮箱/日期为空
                                 # ("17839236545", "xx.zong@idiaoyan.com", "2022/01/01", "autoOpen"),  # 手机邮箱日期更新
                             ])
    def test_put_open_company_info(self, mobile, email, expire_dt, instance_id):
        with allure.step('创建企业'):
            result = self.open_account.put_open_company_info(mobile, email, expire_dt, instance_id)
            if isinstance(result, dict):
                assert result['code'] == 0
                assert result['data'].get("url") is not None
            else:
                assert result.json()['code'] == 204

    @allure.title('租户信息变更异常')
    @pytest.mark.parametrize(("mobile", "email", "expire_dt", "instance_id"),
                             [
                                 ("", "", "", ""),  # 为空
                                 ("", "", "2022/01/02", "autoOpen"),  # 无手机号和邮箱
                                 ("17839236545", "xx.zong@idiaoyan.com", "", "autoOpenEnv"),  # instance_id error
                                 ("17839236545", "xx.zong@idiaoyan.com", "", ""),  # instance_id 为空
                                 ("", "xx.zong@idiaoyan.com", "", "autoOpen"),  # 无手机号有邮箱
                                 ("1", "", "", "autoOpen"),  # 手机号格式错误
                                 (1, "", "", "autoOpen"),  # 手机号类型错误
                                 ("", "1", "", "autoOpen"),  # 邮箱格式错误
                                 ("", 1, "", "autoOpen"),  # 邮箱类型错误
                                 ("", "", "1", "autoOpen"),  # 日期格式错误
                                 ("", "", 1, "autoOpen"),  # 日期类型错误
                                 ("", "", "", 1)  # instance类型错误
                             ])
    def test_put_open_company_info_fail(self, mobile, email, expire_dt, instance_id):
        result = self.open_account.put_open_company_info(mobile, email, expire_dt, instance_id)
        if isinstance(result, dict):
            assert result['code'] != 0
            assert result['code'] != -1
        else:
            assert result.json()['code'] != 0
            assert result.json()['code'] != -1

    @allure.title('累计问卷 / 答卷数查询')
    @pytest.mark.parametrize("dic", (
            {"org_id": "60ab6ba423124d000d106c2c"},
    ))
    def test_get_open_company_quota(self, dic):
        result = self.open_account.get_open_company_quota(**dic)
        assert result['code'] == 0

    @allure.title('获取企业信息')
    @pytest.mark.parametrize("instance_id", (
            ["httprunner27"]
    ))
    def test_get_open_company_info(self, instance_id):
        result = self.open_account.get_open_company_info(instance_id)
        assert result['code'] == 0


if __name__ == '__main__':
    pytest.main(['./tests/test_open_organization'])
# 执行用例
# pytest -q -s tests/test_user/ --clean-alluredir --alluredir=report/report_json/
# 生成报告
#  allure serve report/report_json/
