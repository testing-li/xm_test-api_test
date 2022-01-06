# -*- coding: utf-8 -*-
from api.core.utils import request
from api.core.utils.api_yaml import get_api, _CONFIG
import logging
import sys
import requests

plat_config = _CONFIG['openplatform'][_CONFIG["env"]]


class OpenPlatpormProject:
    def get_open_project_list(self, survey_id, uid, status, start_udt, end_udt, page, rowsPerPage,
                              access_token, re_title=None):
        """
        获取项目列表
        :param org_id: 租户id  yes
        :param survey_id:问卷id，没有时获取所有问卷
        :param uid: 问卷管理员id
        :param status: 问卷状态：（0,未发布）（1,收集中）（2,已结束），没有时获取所有状态问卷。
        :param start_udt: 问卷更新时间区间左端点，2021/03/04 59:59:59
        :param end_udt: 问卷更新时间区间右端点，2021/03/05 59:59:59
        :param page: 页码，默认1
        :param rowsPerPage: 每页数据条数，默认10
        :param re_title: 名称匹配
        :param access_token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        params = {
            'survey_id': survey_id,
            'uid': uid,
            'status': status,
            'start_udt': start_udt,
            'end_udt': end_udt,
            'page': page,
            'rowsPerPage': rowsPerPage,
            're_title': re_title
        }
        return request.get(api, params=params, aes_key=plat_config['aes_key'], token=access_token,
                           env='openplatform')

    def post_open_copy_project(self, title, survey_id, access_token):
        """
        问卷项目复制
        :param title:
        :param survey_id:
        :param access_token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            'title': title,
            'survey_id': survey_id
        }
        return request.post(api, payload=payload, aes_key=plat_config['aes_key'], token=access_token,
                            env='openplatform')

    def post_open_project_data_export(self, survey_id, ex_type, call_back, access_token):
        """
        导出答卷数据
        :param survey_id: 问卷id yes
        :param ex_type:
        (0, 可读数据)
        (1, 按01编码)
        (2, 按非01编码)
        (3, 按非01编码（左对齐）)
        (4, spss-labels-以01显示答卷变量（多选题选项不带题干勾选框未勾选）)
        (5, spss-labels-以非01显示答卷变量（多选题选项不带题干勾选框未勾选）)
        :param call_back: 回调地址 yes
        :param access_token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            'survey_id': survey_id,
            'ex_type': ex_type,
            'call_back': call_back
        }
        return request.post(api, payload=payload, aes_key=plat_config['aes_key'], token=access_token,
                            env='openplatform')

    def post_open_creat_project(self, qdes_title, project_title, access_token):
        """
        创建问卷项目
        :param qdes_title:
        :param project_title:
        :param access_token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            'qdes_title': qdes_title,
            'project_title': project_title
        }
        return request.post(api, payload=payload, aes_key=plat_config['aes_key'], token=access_token,
                            env='openplatform')

    def put_open_project_edit(self, project_id, qdes_title, project_title, access_token):
        """
        编辑问卷/项目名称
        :param project_id:  项目id
        :param qdes_title: 问卷标题
        :param project_title: 项目标题
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            'project_id': project_id,
            'qdes_title': qdes_title,
            'project_title': project_title
        }
        return request.put(api, payload=payload, aes_key=plat_config['aes_key'], token=access_token,
                           env='openplatform')

    def delete_open_project_list(self, project_ids, access_token):
        """
        删除项目列表
        :param project_ids:
        :param access_token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            'project_ids': project_ids,
        }
        return request.delete(api, payload=payload, aes_key=plat_config['aes_key'], token=access_token,
                              env='openplatform')

    def get_open_project_struct_json(self, project_id, version, access_token):
        """
        问卷结构输出
        :param project_id:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        params = {
            'project_id': project_id,
            "version": version
        }
        return request.get(api, params=params, aes_key=plat_config['aes_key'], token=access_token,
                           env='openplatform')

    def get_project_js(self, ID, version):
        if not version:
            version = 0
        api = f'/api/survey/projects/{ID}?version={version}&source=1'
        return request.get(api, env='openplatform')

    def get_open_project_gidmap(self, survey_id, access_token):
        """
        获取问卷gidmap
        :param survey_id:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        params = {
            'survey_id': survey_id,
        }
        return request.get(api, params=params, aes_key=plat_config['aes_key'], token=access_token,
                           env='openplatform')

    def get_open_project_summary(self, project_ids, access_token):
        """
        获取问卷答卷数据统计结果
        :param project_ids:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            'project_ids': project_ids,
        }
        return request.post(api, payload=payload, aes_key=plat_config['aes_key'], token=access_token,
                            env='openplatform')

    def get_open_qdes_export_json(self, survey_id, page, rowsPerPage, start_time_gt, start_time_lte, finish_time_gt,
                                  finish_time_lte, start_seq, access_token):
        """
        答卷数据导出json
        :param survey_id: 问卷id
        :param page: 页码，默认1
        :param rowsPerPage: 每页数据条数，默认10。建议不超过600。
        :param start_time_gt: 答卷开始时间区间左端点， 示例：2021-01-01 12:00:00
        :param start_time_lte:答卷开始时间区间右端点，示例：2021-02-01 12:00:00
        :param finish_time_gt: 答卷结束时间区间左端点
        :param finish_time_lte: 答卷结束时间区间右端点
        :param start_seq: 答卷编号，取该答卷编号之后的答卷，示例6116884
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        params = {
            "survey_id": survey_id,
            "rowsPerPage": rowsPerPage,
            "start_time_gt": start_time_gt,
            "start_time_lte": start_time_lte,
            "page": page,
            "finish_time_gt": finish_time_gt,
            "finish_time_lte": finish_time_lte,
            "start_seq": start_seq
        }
        return request.get(api, params=params, aes_key=plat_config['aes_key'], token=access_token,
                           env='openplatform')
