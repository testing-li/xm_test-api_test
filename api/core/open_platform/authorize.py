#!/usr/bin/env python
# -*- coding: utf-8 -*-
from api.core.utils import request
from api.core.utils.api_yaml import get_api, _CONFIG
import sys


class OpenPlatpormAuthorize:
    def post_access_token(self, org_id, secret_key, app_id=None):
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            "app_id": app_id,
            'org_id': org_id,
            'secret_key': secret_key,
        }
        return request.post(api, payload=payload, aes_key=_CONFIG['openplatform'][_CONFIG["env"]]['aes_key'],
                            env='openplatform')
