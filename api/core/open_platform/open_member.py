# -*- coding: utf-8 -*-
from api.core.utils import request
from api.core.utils.api_yaml import get_api, _CONFIG
import sys


class OpenPlatpormUsers:
    # todo
    def post_open_tag_group(self, access_token):
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        return request.post(api, token=access_token, ID=_CONFIG['openplatform'][_CONFIG["env"]]['plat_code'], env='openplatform')
        pass

    # todo
    def get_open_tag_group(self, access_token):
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        return request.get(api, token=access_token, ID=_CONFIG['openplatform'][_CONFIG["env"]]['plat_code'], env='openplatform')

    def post_open_import_member(self, type, members, access_token):
        """
        联系人导入
        :param type:
        :param members:
        :param import_no:
        :param email:
        :param access_token:
        :param mobile:
        :param name:
        :param gender:
        :param age:
        :param tags:
        :param address:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            'type': type,
            'members': members
        }
        return request.post(api, payload=payload, token=access_token, env='openplatform')

    def get_open_member_import_result(self, task_id, access_token):
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        params = {
            "task_id": task_id
        }
        return request.post(api, params=params, token=access_token, env='openplatform')

    def post_open_creat_member_tag(self, access_token):
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        return request.post(api, token=access_token, ID=_CONFIG['openplatform'][_CONFIG["env"]]['plat_code'], env='openplatform')

    def get_open_member_tag(self, notify, user_list, userName, name, ID, role_title, email, group_ids,
                            access_token):
        """
        用户同步
        :param notify: bool 创建成功是否通知用户
        :param user_list: list 用户信息列表 必填
        :param userName:str 用户名（登录） 必填
        :param name: str  姓名
        :param ID: str 第三方系统用户表示ID 必填
        :param role_title: str 角色名
        :param email: str 用户邮箱 必填
        :param group_ids: list 用户所属层级
        :param access_token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            'notify': notify,
            'user_list': user_list,
            'userName': userName,
            'name': name,
            'ID': ID,
            'role_title': role_title,
            'email': email,
            'group_ids': group_ids
        }
        return request.post(api, payload=payload, token=access_token, env='openplatform')
