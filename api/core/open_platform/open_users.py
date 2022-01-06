# -*- coding: utf-8 -*-
from api.core.utils import request
from api.core.utils.api_yaml import get_api, _CONFIG
import sys


class OpenPlatpormUsers:
    def post_open_user_upload_group(self, filepath, type='excel', access_token=None):
        """
        上传excel层级
        :param filepath:  模板路径
        :param type: 文件类型
        :param access_token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')

        return request.post(api, file=(type, filepath), token=access_token, env='openplatform')

    def get_open_user_group(self, access_token):
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        return request.get(api, token=access_token, env='openplatform')

    def post_open_users(self, user_list, access_token):
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
            'user_list': user_list
        }
        return request.post(api, payload=payload, aes_key=_CONFIG['openplatform'][_CONFIG["env"]]['aes_key'],
                            token=access_token, env='openplatform')

    def get_open_users(self, userName, status, email, mobile, access_token):
        """
        获取账号列表
        :param userName: 需要进行查询账号的用户名
        :param status: 账号状态（0，激活中）（1，已激活）（2，已禁用）
        :param email: 需要进行查询的账号的邮箱
        :param mobile: 需要进行查询的账号的手机号
        :param access_token: token
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        params = {
            'userName': userName,
            'status': status,
            'email': email,
            'mobile': mobile
        }
        return request.get(api, params=params, aes_key=_CONFIG['openplatform'][_CONFIG["env"]]['aes_key'],
                            token=access_token, env='openplatform')

    def post_open_user_group(self, access_token, groupLevelList, groupList):
        """
        传入全量有效的层级数据来同步层级
        :param access_token:
        :param kwargs:
        groupLevelList	list
        title	str	层级名称
        level	int	层级数
        groupList	list
        code	str	组织编码（不可重复）
        adminName	str	组织负责人
        title	str	组织名称 （不可重复）
        praentCode	str	上级组织编码(根节点为空)
        is_root	bool	是否是根节点(只有一个根节点)
        :return: code data
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            "groupLevelList": groupLevelList,
            "groupList": groupList
        }

        return request.post(api, payload=payload, token=access_token,
                            aes_key=_CONFIG['openplatform'][_CONFIG["env"]]['aes_key'], env='openplatform')
