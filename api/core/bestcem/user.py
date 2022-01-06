# -*- coding: utf-8 -*-
from api.core.utils import request
from api.core.utils.api_yaml import get_api
import sys


class Authorize:
    def post_company_token(self, org_code, user_name, password):
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            'is_home_page': False,
            'org_code': org_code,
            'user_name': user_name,
            'password': password
        }
        return request.post(api, payload=payload)


class User:
    def get_company(self, token=None):
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        return request.get(api, token=token)

    def get_self(self, token=None):
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        return request.get(api, token=token)


if __name__ == '__main__':
    # s = Authorize()
    # s.post_company_token(1,2,1)
    User().get_self()
