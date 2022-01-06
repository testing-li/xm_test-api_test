#!/usr/bin/env python
# -*- coding: utf-8 -*-
from api.core.utils import request
from api.core.utils.api_yaml import get_api, _CONFIG
from api.core.utils import sign_utils
import urllib.parse
import json
import sys

plat_config = _CONFIG['openplatform'][_CONFIG["env"]]


class OpenPlatformOrganization:

    def post_open_creat_account(self, code, name, mobile, email, expire_dt, instance_id, **kwargs):
        """
        租户创建
        :param code: 组织编码，示例：sample str
        :param name: 公司名称，示例：sample str
        :param mobile: requirement 手机号 str
        :param email: 邮箱 str
        :param expire_dt: 过期时间，格式：2021/03/23 为空时默认在一年后
        :param instance_id: requirement 标识租户的唯⼀ID，第三方系统的租户标识
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        params = {
            'code': code,
            'name': name,
            'mobile': mobile,
            'email': email,
            'expire_dt': expire_dt,
            'instance_id': instance_id,
            'package': kwargs.get("package", None)
        }
        payload = {}
        for k, v in params.items():
            if v is not None:
                payload[k] = v
        sign_params = {
            "method": "POST",
            "url": f"{api.format(ID=plat_config['plat_code'])}",
            "body": json.dumps(payload),
            "key": plat_config['platform_key']
        }
        sign = sign_utils.gen_sign(sign_params)
        headers = {
            "platformcode": plat_config['plat_code'],
            "Platform-Sign": sign
        }
        return request.post(api, payload=payload, ID=plat_config['plat_code'],
                            aes_key=plat_config['platform_key'], env='openplatform', headers=headers)

    def put_open_company_info(self, mobile, email, expire_dt, instance_id, **kwargs):
        """
        租户信息变更
        :param mobile: requirement 手机号
        :param email:
        :param expire_dt:
        :param instance_id: requirement 标识租户的唯⼀ID，第三方系统的租户标识
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        params = {
            'mobile': mobile,
            'email': email,
            'expire_dt': expire_dt,
            'instance_id': instance_id,
            'package': kwargs.get("package", None)
        }
        payload = {}
        for k, v in params.items():
            if v is not None:
                payload[k] = v
        sign_params = {
            "method": "PUT",
            "url": f"{api.format(ID=plat_config['plat_code'])}",
            "body": json.dumps(payload),
            "key": plat_config['platform_key']
        }
        sign = sign_utils.gen_sign(sign_params)
        headers = {
            "platformcode": plat_config['plat_code'],
            "Platform-Sign": sign
        }
        return request.put(api, payload=payload, ID=plat_config['plat_code'],
                           aes_key=plat_config['platform_key'], env='openplatform', headers=headers)

    def get_open_company_info(self, instance_id):
        """
        租户创建信息重新获取
        :param instance_id:  requirement 标识租户的唯⼀ID，第三方系统的租户标识
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        params = {
            'instance_id': instance_id
        }
        sign_params = {
            "method": "GET",
            "url": f"{api.format(ID=plat_config['plat_code'])}?{urllib.parse.urlencode(params)}",
            "body": '',
            "key": plat_config['platform_key']
        }
        print(sign_params)
        sign = sign_utils.gen_sign(sign_params)
        headers = {
            "platformcode": plat_config['plat_code'],
            "Platform-Sign": sign
        }
        return request.get(api, params=params, ID=plat_config['plat_code'],
                           aes_key=plat_config['platform_key'], env='openplatform', headers=headers)

    def get_open_company_quota(self, **kwargs):
        """
        累计问卷 / 答卷数查询
        :param kwargs:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        params = {
            'page': kwargs.get('page'),
            "rowsPerPage": kwargs.get('rowsPerPage'),
            "project_gt": kwargs.get('project_gt'),
            "project_lte": kwargs.get('project_lte'),
            "respondent_gt": kwargs.get('respondent_gt'),
            "respondent_lte": kwargs.get('respondent_lte'),
            "org_id": kwargs.get('org_id'),
        }
        real_params = {k: v for k, v in params.items() if v is not None}
        sign_params = {
            "method": "GET",
            "url": f"{api.format(ID=plat_config['plat_code'])}?{urllib.parse.urlencode(real_params)}",
            "body": "{}",
            "key": plat_config['platform_key']
        }
        headers = {
            "platformcode": plat_config['plat_code'],
            "Platform-Sign": sign_utils.gen_sign(sign_params)
        }
        return request.get(api, params=params, ID=plat_config['plat_code'],
                           aes_key=plat_config['platform_key'], env='openplatform', headers=headers)


if __name__ == '__main__':
    d = {
        "instance_id": "httprunner22"
    }
    s = OpenPlatformOrganization()
    t = s.get_open_company_info(instance_id="httprunner22")
    # t = s.get_open_company_quota(**d)
