#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import pytest
from api.core.utils import api_yaml, request
from api.utils import log
from api.utils import read_yaml
from api.utils import send_email
import time

_config = read_yaml.read_yaml("/config.yaml")
log.Logging()


def pytest_runtest_call(__multicall__):
    try:
        __multicall__.execute()
    except KeyboardInterrupt:
        raise
    except:
        logging.exception('pytest_runtest_call caught exception:')
        raise


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    收集测试结果 发送测试报告
    :param terminalreporter:
    :param exitstatus:
    :param config:
    :return:
    """
    total = terminalreporter._numcollected
    passed = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    failed = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    error = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    skipped = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    success_rate = len(terminalreporter.stats.get('passed', [])) / terminalreporter._numcollected * 100
    duration = time.time() - terminalreporter._sessionstarttime
    data = f'total: {total}, passed: {passed}, failed: {failed}, error: {error}, skipped: {skipped}, success_rate: {success_rate:.2f}%, times: {duration:.2f}s'
    logging.info(data)
    flag = _config['email']['flag']
    stmp_address = _config['email']['stmp_address']
    stmp_password = _config['email']['stmp_password']
    stmp_server = _config['email']['stmp_server']
    stmp_port = _config['email']['stmp_port']
    send_to = _config['email']['send_to']
    mail_msg = f'<p>API测试运行完成</p><p>执行情况: {data}</p><p>点击 <a href=http://{_config["report_address"]["ip"]}:{_config["report_address"]["host"]}>查看详情</a></p>'
    send_email.sendReport(flag, send_to, stmp_address, stmp_password, stmp_server, stmp_port, file=None, text=mail_msg,
                          textType='html')


@pytest.fixture(scope='session')
def set_headers(user='admin_user'):
    url = f'{_config["env"]["bestcem"]}/api/authorize/v2/token/'
    user = api_yaml.get_user(user)
    payload = {
        'is_home_page': False,
        'org_code': user['org_code'],
        'user_name': user['user_name'],
        'password': user['password']
    }
    result = request.post(url, payload=payload, env=False)
    token = f"Bearer {result.json()['data']['token']}"
    return token



