#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import allure
from api.core.open_platform import open_event
from api.core.utils.api_yaml import _CONFIG

plat_config = _CONFIG['openplatform'][_CONFIG["env"]]


@allure.feature('open_event')
@allure.severity(allure.severity_level.NORMAL)
class TestOpenEvent:
    apis = open_event.OpenPlatformEvent()

    # 生成投放链接
    @allure.title('添加事件订阅配置')
    @pytest.mark.parametrize(('callback_api', "enable"),
                             [
                                 ("http://276a-116-232-54-20.ngrok.io/openplatform/survey_submit", True)
                             ])
    def test_post_open_event_subscribe(self, callback_api, enable, set_access_token):
        with allure.step('获取链接'):
            result = self.apis.post_open_event_subscribe(callback_api=callback_api, enable=enable,
                                                         access_token=set_access_token)
            assert result['code'] == 0


if __name__ == '__main__':
    pytest.main()
# 执行用例
# pytest -q -s tests/test_user/ --clean-alluredir --alluredir=report/report_json/
# 生成报告
#  allure serve report/report_json/
