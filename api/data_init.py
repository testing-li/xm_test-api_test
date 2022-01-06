#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from api.core.utils import request
from api.utils import log
from api.utils import read_yaml

_config = read_yaml.read_yaml("/config.yaml")
log.Logging()


def init_openplatform_account(code="openlatform", instance_id="openlatform"):
    if not _config['openplatform'][_config['env']]['secret_key']:
        url = f'{_config["base_url"][_config["env"]]["openplatform"]}/api/open/v1/organization/{_config["openplatform"][_config["env"]]["plat_code"]}'
        payload = {
            "code": code,
            "name": "众言科技",
            "mobile": "17839236545",
            "email": "xx.zong@idiaoyan.com",
            "expire_dt": "2022/01/01",
            "instance_id": instance_id
        }
        result = request.post(url, payload=payload, env=False,
                              aes_key=_config['openplatform'][_config["env"]]['platform_key'])
        if result['code'] == 0:
            data = {
                "openplatform": {
                    _config["env"]:
                        {"secret_key": result['data']['secret_key'],
                         "aes_key": result['data']['aes_key'],
                         "org_id": result['data']['org_id']}
                }
            }
            read_yaml.rewirte_yaml('/config.yaml', data)
            logging.info("平台账号初始化")
        else:
            logging.info('账号初始化失败')
            exit()


def init_openplatform_project():
    auto_url = f'{_config["base_url"][_config["env"]]["openplatform"]}/api/open/v1/auth/platform/'
    project_url = f'{_config["base_url"][_config["env"]]["openplatform"]}/api/open/v1/project/'
    if _config['openplatform'][_config["env"]]['default_survey_id']:
        logging.info('默认问卷id已存在')
    elif not _config['openplatform']['secret_key']:
        logging.info('secret_key不存在')
    else:
        payload = {
            'org_id': _config['openplatform'][_config["env"]]['org_id'],
            'secret_key': _config['openplatform'][_config["env"]]['secret_key']
        }
        result = request.post(auto_url, payload=payload, env=False)
        token = f"Bearer {result.json()['data']['access_token']}"
        project_list = request.get(project_url, env=False, token=token,
                                   aes_key=_config['openplatform'][_config["env"]]['aes_key'])
        if project_list['code'] == 0 and project_list['data'].get('rows'):
            data = {
                "openplatform": {"default_survey_id": project_list['data'].get('rows')[0].get('survey_id')}}
            read_yaml.rewirte_yaml('/config.yaml', data)
            logging.info("初始化记录示例问卷")
        else:
            logging.info('项目不存在，请检查项目列表并创建答卷数据')


if __name__ == '__main__':
    init_openplatform_account(code='opentest525', instance_id='opentestf525')
    init_openplatform_project()
