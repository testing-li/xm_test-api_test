#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import allure
from api.core.open_platform import authorize
from api.core.utils.api_yaml import _CONFIG

plat_config = _CONFIG['openplatform'][_CONFIG["env"]]


@allure.feature('open_authorize')
@allure.severity(allure.severity_level.BLOCKER)
class TestAuthorize:
    apis = authorize.OpenPlatpormAuthorize()

    @allure.title('获取access_token')
    @pytest.mark.parametrize(('org_id', 'secret_key', "app_id"),
                             [
                                 # (plat_config['org_id'], plat_config['secret_key'], None),
                                 ("5fc8b996aace70000cb1ac2b",
                                  "82E24w4eGCS0KA2s0UypQ99934lTk7E16Q64r589wO6pfLNwXNXpl58H81247529", None)
                                 # ("61285f42b6079a22ec529ee1", "iq944h4HMNliEe455123Xv6X8HZkBi1t20y7975nGi6au1Ofq7491f2017M03jO2", "612b5697594a3937305cd10a"),
                                 # (plat_config['app_org_id'], plat_config['app_secret_key'], plat_config['app_id']),
                                 # (plat_config['app_org_id'], plat_config['app_secret_key'], None),
                             ]
                             )
    def test_post_access_token(self, org_id, secret_key, app_id):
        result = self.apis.post_access_token(org_id, secret_key, app_id)
        assert result.json()['code'] == 0
        assert result.json()['data'].get("access_token") is not None

    @allure.title('获取access_token fail')
    @pytest.mark.parametrize(('org_id', 'secret_key', "app_id"),
                             [
                                 (plat_config['org_id'], plat_config['platform_key'], None),
                                 (plat_config['app_org_id'], None, plat_config['app_id']),
                                 (plat_config['app_org_id'], plat_config['app_secret_key'], 1),
                                 (plat_config['app_org_id'],
                                  "3aEgcEhZDrM46ol6z6Va7Nh26089j66CSu2Wu104jcZus63007g584z57W56114M",
                                  plat_config['app_id']),
                                 (plat_config['env_org_id'], plat_config['secret_key'], None),
                                 (plat_config['org_id'], "", None),
                                 ("", plat_config['platform_key'], None),
                                 ("", "", None),
                                 (1, "", None),
                                 (plat_config['org_id'], 1, None)
                             ]
                             )
    def test_post_access_token_fail(self, org_id, secret_key, app_id):
        result = self.apis.post_access_token(org_id, secret_key, app_id)
        if isinstance(result, dict):
            assert result['code'] != 0
            assert result['code'] != -1
        else:
            assert result.json()['code'] != 0
            assert result.json()['code'] != -1


if __name__ == '__main__':
    pytest.main(['./test_open_authorize.py'])

# 执行用例
# pytest -q -s tests/test_user/ --clean-alluredir --alluredir=report/report_json/
# 生成报告
#  allure serve report/report_json/
