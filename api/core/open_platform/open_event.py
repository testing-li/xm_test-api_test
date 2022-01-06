# -*- coding: utf-8 -*-
from api.core.utils import request
from api.core.utils.api_yaml import get_api, _CONFIG
import sys

plat_config = _CONFIG['openplatform'][_CONFIG["env"]]


class OpenPlatformEvent:
    def post_open_event_subscribe(self, callback_api, enable, access_token):
        """
        添加事件订阅配置
        :param callback_api: 接受事件的api全路径
        :param enable: 接受事件使能
        :param access_token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            "subscribe": {
                'api': callback_api,
                'enable': enable
            }}
        return request.post(api, payload=payload, aes_key=plat_config['aes_key'], token=access_token,
                            env='openplatform')
