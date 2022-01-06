#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import allure
from api.utils.read_yaml import write_yaml
from api.core.open_platform import open_deliver
from api.core.utils.api_yaml import _CONFIG
from api.core.utils import sign_utils

plat_config = _CONFIG['openplatform'][_CONFIG["env"]]


@allure.feature('open_deliver')
@allure.severity(allure.severity_level.NORMAL)
class TestOpenOraganization:
    apis = open_deliver.OpenPlatpormDeliver()

    # 生成投放链接
    @allure.title('生成投放链接')
    @pytest.mark.parametrize(('survey_id', "type", "page", "rowsPerPage"),
                             [
                                 (plat_config['default_survey_id'], 0, 1, 100)
                                 # ("610bb0cd8c51f29efca9d3d8", 0, 1, 10)
                             ])
    def test_post_open_creat_deliver_third(self, survey_id, type, page, rowsPerPage, set_access_token):
        with allure.step('获取链接'):
            result = self.apis.post_open_creat_deliver_third(survey_id, type, page, rowsPerPage,
                                                             set_access_token)
            assert result['code'] == 0
            assert result['data']['total'] != 0
            data = result['data'].get('rows')
            assert data is not None
            assert data[0]['link_total'] != 0
            assert data[0]['link_rows'][0].get('link') is not None
        with allure.step('外部参数拼接'):
            deliver_list = []
            for i in data:
                for j in i['link_rows']:
                    link = j.get('link')
                    if link:
                        third_params = {'int1': 15, "str1": 'test123', "bool1": 'false'}
                        third_link = sign_utils.regen_params(link, third_params)
                        deliver_list.append(third_link)
                        assert third_link is not None
            write_yaml(deliver_list, '/data/deliver_list.yaml')

    @allure.title('生成投放链接异常')
    @pytest.mark.parametrize(('survey_id', "type", "page", "rowsPerPage"),
                             [
                                 # (plat_config['default_survey_id'], 3, 1, 100), 空
                                 # (plat_config['default_survey_id'], 0, 1, '100'), 有数据
                                 # (plat_config['default_survey_id'], "1", 1, 10),  空
                                 # ("60a63d33aace700009d6c5fb", 0, 1, 10),  空
                                 ("", 0, 1, 10),
                                 (1, 0, 1, 10)
                             ])
    def test_post_open_creat_deliver_third_fail(self, survey_id, type, page, rowsPerPage, set_access_token):
        result = self.apis.post_open_creat_deliver_third(survey_id, type, page, rowsPerPage,
                                                         set_access_token)
        if isinstance(result, dict):
            assert result['code'] != 0
            assert result['code'] != -1
        else:
            assert result.json()['code'] != 0
            assert result.json()['code'] != -1


if __name__ == '__main__':
    pytest.main()
# 执行用例
# pytest -q -s tests/test_user/ --clean-alluredir --alluredir=report/report_json/
# 生成报告
#  allure serve report/report_json/
