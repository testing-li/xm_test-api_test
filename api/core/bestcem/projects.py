# -*- coding: utf-8 -*-
from api.core.utils import request
from api.core.utils.api_yaml import get_api
import sys


class Projects:
    # do
    def post_creat_project(self, title, folder_id, token=None):
        """
        普通创建项目
        :param title: 项目标题
        :param folder_id: 文件夹id
        :param token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            "title": title, "folder_id": folder_id
        }
        return request.post(api, payload=payload, token=token)

    def delete_project(self, project_id=None, token=None):
        """
        :param pid: project_id
        :param token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            "pid": project_id
        }
        return request.delete(api, payload=payload, token=token)

    def put_project(self, status: int, project_id: str, token=None):
        """
        激活，结束项目
        :param status: 1，激活  2 结束
        :param project_id: 项目id
        :param token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            "pid": project_id, "status": status
        }
        return request.put(api, payload=payload, token=token)

    def post_lib_creat_project(self, lib_id, folder_id='', title='', token=None):
        """
        通过模板创建项目
        :param lib_id: 模板id
        :param folder_id: 文件夹id
        :param title: 项目标题
        :param token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            "title": title, "folder_id": folder_id
        }
        return request.post(api, payload=payload, ID=lib_id, token=token)

    # do
    def post_copy_project(self, project_id, title=None, folder_id=None, token=None):
        """
        复制项目
        :param project_id: 复制项目的项目ID
        :param title: 创建项目的标题
        :param folder_id: 创建项目所属的问价夹ID
        :param token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            "title": title,
            "folder_id": folder_id
        }
        return request.post(api, payload=payload, ID=project_id, token=token)

    def put_move_project(self, projectID=None, folder_id=None, token=None):
        """
        移动项目
        :param projectID: 项目ID
        :param folder_id: 文件夹id
        :param token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            "folder_id": folder_id
        }
        return request.put(api, ID=projectID, payload=payload, token=token)

    # do
    def post_import_project(self, file=None, type='excel', token=None):
        """
        上传excel项目
        :param filepath:  模板路径
        :param type: 文件类型
        :param token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        params = {
            "type": type
        }
        return request.post(api, params=params, file=file, token=token)

    def post_import_project_qstruct(self, sid, folder_id=None, title=None, token=None):
        """
        excel上传项目确定保存生成项目
        :param sid: excel生成文件的sid
        :param folder_id: 文件夹id
        :param title: 项目名称
        :param token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            "folder_id": folder_id,
            "title": title
        }
        return request.post(api, payload=payload, ID=sid, token=token)

    def put_project_title(self, project_id, title='', token=None):
        """
        修改项目标题
        :param project_id: 项目ID，路径
        :param title: 项目标题
        :param token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            "title": title
        }
        return request.put(api, ID=project_id, payload=payload, token=token)

    def get_project_list(self, title=None, status=None, folder_id=None, page=1, rowsPerPage=10, token=None):
        """
        :param title: 项目标题，模糊搜索
        :param status: 项目状态：0，1，2
        :param folder_id: 所属文件夹
        :param page: 第几页
        :param rowsPerPage: 每页条数
        :param token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        params = {
            "title": title,
            "status": status,
            "folder_id": folder_id,
            "page": page,
            "rowsPerPage": rowsPerPage
        }
        return request.get(api, params=params, token=token)

    def post_project_release(self, project_id, force=False, token=None):
        """
        问卷发布更新
        :param project_id: 项目ID
        :param force: boolean 默认false
        :param token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            "force": force
        }
        return request.post(api, ID=project_id, payload=payload, token=token)

    def get_project_share_users(self, project_id, token=None):
        """
        获取项目的被分享人列表
        :param project_id: 项目ID
        :param token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        return request.post(api, ID=project_id, token=token)

    def post_project_share(self, project_id, projects, token=None):
        """
        分享项目
        :param project_id: 项目id
        :param projects: userid, permissions[list]
        permissions: 项目管理：10 11 12
        问卷：20，21，22
        行动：41，42，43
        投放：60，61
        数据报表：81-92
        答卷数据权限管理：100，102，103
        工单数据权限管理：120，122，123
        :param token:
        :return:
        """
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            "projects": projects
        }
        return request.post(api, ID=project_id, payload=payload, token=token)

    def get_project_share(self, project_id, user_id, token=None):
        """
        用户分享权限的查看
        :param project_id: 项目id
        :param user_id: 用户id
        :param token:
        :return:
        """
        params = {
            "user_id": user_id
        }
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        return request.post(api, ID=project_id, params=params, token=token)

    def get_project_search_user(self, project_id, keyword='', token=None):
        """
        关键字搜索可分享用户
        :param project_id:
        :param keyword: 关键字
        :param token:
        :return:
        """
        params = {
            "keyword": keyword
        }
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        return request.post(api, ID=project_id, params=params, token=token)
