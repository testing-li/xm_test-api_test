# -*- coding: utf-8 -*-
from api.core.utils import request
from api.core.utils.api_yaml import get_api, _CONFIG
import sys


class OpenPlatpormDeliver:
    def post_open_creat_deliver_third(self, survey_id, type, page, rowsPerPage,
                                      access_token):
        """
        投放链接获取
        :param org_id:
        :param survey_id:
        :param ttype: 问卷类型，（0，不区分层级）（1，区分层级）
        :param page: 页码，默认1。当survey_id为多个时不生效。
        :param rowsPerPage: 每页数据条数，默认10。当survey_id为多个时不生效。
        :param access_token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            'survey_id': survey_id,
            'ttype': type
        }
        params = {
            'page': page,
            'rowsPerPage': rowsPerPage
        }
        return request.post(api, params=params, payload=payload,
                            aes_key=_CONFIG['openplatform'][_CONFIG["env"]]['aes_key'],
                            token=access_token, env='openplatform')
