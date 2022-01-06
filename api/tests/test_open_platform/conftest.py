#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import pytest
from api.core.utils import api_yaml, request
from api.utils import log
from api.core.utils.api_yaml import _CONFIG

plat_config = _CONFIG['openplatform'][_CONFIG["env"]]
base_url = _CONFIG["base_url"][_CONFIG["env"]]
log.Logging()


@pytest.fixture(scope='session')
def set_access_token():
    url = f'{base_url["openplatform"]}/api/open/v1/auth/platform/'
    payload = {
        'org_id': plat_config['org_id'],
        'secret_key': plat_config['secret_key']
    }
    result = request.post(url, payload=payload, env=False)
    token = f"Bearer {result.json()['data']['access_token']}"
    return token

