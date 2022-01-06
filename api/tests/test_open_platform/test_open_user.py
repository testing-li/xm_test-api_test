# -*- coding: utf-8 -*-
import pytest
import allure
from api.core.open_platform import open_users
from api.utils import method, getDir


@allure.feature('user')
class TestOpenOraganization:
    apis = open_users.OpenPlatpormUsers()

    @allure.title('上传组织层级')
    def test_post_open_user_group(self, set_access_token):
        filePath = f'{getDir.proDir}/data/file/group_demo.xlsx'
        result = self.apis.post_open_user_upload_group(filepath=filePath, access_token=set_access_token)
        assert result['code'] == 0
        assert result['data']['msg'] == 'success'

    @allure.title('获取组织层级')
    def test_get_open_user_group(self, set_access_token):
        result = self.apis.get_open_user_group(access_token=set_access_token)
        assert result['code'] == 0
        assert result['data']['groups'][0]['code'] == 'A01'

    @allure.title('账号列表查询')
    @pytest.mark.parametrize(("userName", "status", "email", "mobile"),
                             [
                                 ("superadmin", None, "xx.zong@123.1222222.com", None),
                                 # (None, 0, None, None,),
                                 # (None, 1, None, None),
                                 # (None, 2, None, None,),
                                 (None, None, None, None,),
                                 # (None, None, "xx.zong@idiaoyan.com", None),
                                 # (None, None, None, "17839236545"),
                                 # ("superadmin", 1, "xx.zong@idiaoyan.com", "17839236545"),
                             ])
    def test_get_open_users(self, userName, status, email, mobile, set_access_token):
        result = self.apis.get_open_users(userName, status, email, mobile, access_token=set_access_token)
        assert result['code'] == 0
        assert result['data'][0].get('orgID') is not None
        assert result['data'][0].get("userName") is not None
        if userName:
            assert result['data'][0].get("userName") == userName
        if status:
            assert result['data'][0].get("status") == status
        if email:
            assert result['data'][0].get("email") == email
        if mobile:
            assert result['data'][0].get("mobile") == mobile

    @allure.title('账号列表查询为空')
    @pytest.mark.parametrize(("userName", "status", "email", "mobile"),
                             [
                                 ("testselect", None, None, None),
                                 (None, 4, None, None,),
                                 (None, None, "xx.zong123@idiaoyan.com", None),
                                 (None, None, None, "15499999999"),
                                 ("superadmin", 0, "xx.zong@idiaoyan.com", "17839236545"),
                             ])
    def test_get_open_users_null(self, userName, status, email, mobile, set_access_token):
        result = self.apis.get_open_users(userName, status, email, mobile, access_token=set_access_token)
        assert result['code'] == 0
        assert result['data'] == []

    @allure.title('账号列表查询异常case')
    @pytest.mark.parametrize(("userName", "status", "email", "mobile"),
                             [
                                 (1, None, None, None),
                                 (None, "test", None, None,),
                                 (None, None, 1, None),
                                 (None, None, None, 1),
                             ])
    def test_get_open_users_fail(self, userName, status, email, mobile, set_access_token):
        result = self.apis.get_open_users(userName, status, email, mobile, access_token=set_access_token)
        if isinstance(result, dict):
            assert result['code'] != 0
            assert result['code'] != -1
        else:
            assert result.json()['code'] != 0
            assert result.json()['code'] != -1

    # todo 增加测试用例
    # todo 增加失败用例
    @allure.title('新增子账号')
    @pytest.mark.parametrize(("user_list"),
                             [
                                 ([[f"user{method.strNum(3)}", f"name{method.strNum(3)}",
                                    f"instanceId{method.strNum(3)}", 'test1', "ssss", []]])
                             ])
    def test_post_open_users(self, user_list, set_access_token):
        base_list = ['userName', 'name', 'ID', 'role_title', 'email', "group_ids"]
        dict_user_list = []
        for i in user_list:
            dict_user_list.append(dict(zip(base_list, i)))
        result = self.apis.post_open_users(dict_user_list, access_token=set_access_token)
        assert result['code'] == 0
        assert result['data'].get('success') is not None

    @allure.title('导入组织层级')
    @pytest.mark.parametrize(("groupLevelList", "groupList"),
                             [
                                 (method.generate_group_level(4),
                                  method.generate_group_organization(4, 5, 4, 5, basecode="test")),
                                 # (method.generate_group_level(5), method.generate_group_organization(5, 10, 10, 10, 5)),
                                 # (method.generate_group_level(2), method.generate_group_organization(2, 10)),
                                 # (method.generate_group_level(3), method.generate_group_organization(3, 10, 5)),
                                 # (method.generate_group_level(3),
                                 #  method.generate_group_organization(3, 10, 5, basecode="hello")[:-1])
                             ])
    def test_post_open_user_group(self, groupLevelList, groupList, set_access_token):
        result = self.apis.post_open_user_group(access_token=set_access_token, groupLevelList=groupLevelList,
                                                groupList=groupList)
        assert result['code'] == 0

    @allure.title('导入组织层级异常cese')
    @pytest.mark.parametrize(("groupLevelList", "groupList"),
                             [
                                 # 层级为空
                                 ([], []),
                                 # 组织为空
                                 (method.generate_group_level(3), []),
                                 # 组织层级不匹配
                                 (method.generate_group_level(3), method.generate_group_organization(4, 2, 2, 2)),
                                 # 多个根节点
                                 (method.generate_group_level(3), [{
                                     'code': 'code0',
                                     'adminName': 'name0',
                                     'title': 'org0',
                                     'parentCode': '',
                                     'is_root': True
                                 }, {
                                     'code': 'code0_0',
                                     'adminName': 'name0_0',
                                     'title': 'org0_0',
                                     'parentCode': '',
                                     'is_root': True
                                 }]),
                                 # 缺少根节点
                                 (method.generate_group_level(3), [{
                                     'code': 'code0',
                                     'adminName': 'name0',
                                     'title': 'org0',
                                     'parentCode': '123',
                                     'is_root': False
                                 }, {
                                     'code': 'code0_0',
                                     'adminName': 'name0_0',
                                     'title': 'org0_0',
                                     'parentCode': '123',
                                     'is_root': False
                                 }]),
                                 # 节点环绕
                                 (method.generate_group_level(3), [{
                                     'code': 'code0',
                                     'adminName': 'name0',
                                     'title': 'org0',
                                     'parentCode': '',
                                     'is_root': True
                                 }, {
                                     'code': 'code0_0',
                                     'adminName': 'name0_0',
                                     'title': 'org0_0',
                                     'parentCode': 'code0_1',
                                     'is_root': False
                                 }, {
                                     'code': 'code0_1',
                                     'adminName': 'name0_0',
                                     'title': 'org0_0',
                                     'parentCode': 'code0_0',
                                     'is_root': False
                                 }]),
                                 # parent_code not found
                                 (method.generate_group_level(3), [{
                                     'code': 'code0',
                                     'adminName': 'name0',
                                     'title': 'org0',
                                     'parentCode': '',
                                     'is_root': True
                                 }, {
                                     'code': 'code0_0',
                                     'adminName': 'name0_0',
                                     'title': 'org0_0',
                                     'parentCode': 'code1',
                                     'is_root': False
                                 }]),
                                 # code重复
                                 (method.generate_group_level(3), [{
                                     'code': 'code0',
                                     'adminName': 'name0',
                                     'title': 'org0',
                                     'parentCode': '',
                                     'is_root': True
                                 }, {
                                     'code': 'code0_0',
                                     'adminName': 'name0_0',
                                     'title': 'org0_0',
                                     'parentCode': 'code0',
                                     'is_root': False
                                 }, {
                                     'code': 'code0_0',
                                     'adminName': 'name0_0',
                                     'title': 'org0_1',
                                     'parentCode': 'code0',
                                     'is_root': False
                                 }]),
                                 # title重复
                                 (method.generate_group_level(3), [{
                                     'code': 'code0',
                                     'adminName': 'name0',
                                     'title': 'org0',
                                     'parentCode': '',
                                     'is_root': True
                                 }, {
                                     'code': 'code0_0',
                                     'adminName': 'name0_0',
                                     'title': 'org0_0',
                                     'parentCode': 'code0',
                                     'is_root': False
                                 }, {
                                     'code': 'code0_1',
                                     'adminName': 'name0_0',
                                     'title': 'org0_0',
                                     'parentCode': 'code0',
                                     'is_root': False
                                 }]),
                                 # code为None
                                 (method.generate_group_level(3), [{
                                     'code': None,
                                     'adminName': 'name0',
                                     'title': 'org0',
                                     'parentCode': '',
                                     'is_root': True
                                 }]),
                                 # code超过32
                                 (method.generate_group_level(3), [{
                                     "code": method.lowercase(33),
                                     'adminName': 'name0',
                                     'title': method.lowercase(33),
                                     'parentCode': '',
                                     'is_root': True
                                 }]),
                                 # code缺失
                                 (method.generate_group_level(3), [{
                                     'adminName': 'name0',
                                     'title': 'org0',
                                     'parentCode': '',
                                     'is_root': True
                                 }]),
                                 # code非字母下划线
                                 (method.generate_group_level(3), [{
                                     "code": "#test",
                                     'adminName': 'name0',
                                     'title': 'org0',
                                     'parentCode': '',
                                     'is_root': True
                                 }]),
                                 # code类型  fail
                                 (method.generate_group_level(3), [{
                                     "code": 1,
                                     'adminName': 'name0',
                                     'title': 'org0',
                                     'parentCode': '',
                                     'is_root': True
                                 }]),
                                 # title为None
                                 (method.generate_group_level(3), [{
                                     'code': "code0",
                                     'adminName': 'name0',
                                     'title': None,
                                     'parentCode': '',
                                     'is_root': True
                                 }]),
                                 # title缺失
                                 (method.generate_group_level(3), [{
                                     'code': "code0",
                                     'adminName': 'name0',
                                     'parentCode': '',
                                     'is_root': True
                                 }]),
                                 # title为空字符
                                 (method.generate_group_level(3), [{
                                     "code": "code0",
                                     'adminName': 'name0',
                                     'title': '',
                                     'parentCode': '',
                                     'is_root': True
                                 }]),
                                 # title超过32
                                 (method.generate_group_level(3), [{
                                     "code": "code0",
                                     'adminName': 'name0',
                                     'title': method.lowercase(33),
                                     'parentCode': '',
                                     'is_root': True
                                 }]),
                                 # code not str   fail
                                 (method.generate_group_level(3), [{
                                     "code": [],
                                     'adminName': 'name0',
                                     'title': "title1",
                                     'parentCode': '',
                                     'is_root': True
                                 }]),
                                 # title not str
                                 (method.generate_group_level(3), [{
                                     "code": "code0",
                                     'adminName': 'name0',
                                     'title': 1,
                                     'parentCode': '',
                                     'is_root': True
                                 }]),
                                 # is root not boolean   fail
                                 (method.generate_group_level(3), [{
                                     "code": "code0",
                                     'adminName': 'name0',
                                     'title': "title1",
                                     'parentCode': '',
                                     'is_root': "false"
                                 }]),
                                 # is_root None
                                 (method.generate_group_level(3), [{
                                     "code": "code0",
                                     'adminName': 'name0',
                                     'title': "title1",
                                     'parentCode': '',
                                     'is_root': None
                                 }]),
                                 # parentCode 多个为空
                                 (method.generate_group_level(3), [{
                                     'code': 'code0',
                                     'adminName': 'name0',
                                     'title': 'org0',
                                     'parentCode': '',
                                     'is_root': True
                                 }, {
                                     'code': 'code0_0',
                                     'adminName': 'name0_0',
                                     'title': 'org0_0',
                                     'parentCode': '',
                                     'is_root': None
                                 }]),
                                 # adminName is None
                                 (method.generate_group_level(3), [{
                                     "code": "code0",
                                     'adminName': None,
                                     'title': "title1",
                                     'parentCode': '',
                                     'is_root': None
                                 }]),
                                 # adminName not str
                                 (method.generate_group_level(3), [{
                                     "code": "code0",
                                     'adminName': 1,
                                     'title': "title1",
                                     'parentCode': '',
                                     'is_root': None
                                 }]),
                             ])
    def test_post_open_user_group_error(self, groupLevelList, groupList, set_access_token):
        result = self.apis.post_open_user_group(access_token=set_access_token, groupLevelList=groupLevelList,
                                                groupList=groupList)
        if isinstance(result, dict):
            assert result['code'] != 0
            assert result['code'] != -1
        else:
            assert result.json()['code'] != 0
            assert result.json()['code'] != -1


if __name__ == '__main__':
    pytest.main(['./test_open_project.py'])
# 执行用例
# pytest -q -s tests/test_user/ --clean-alluredir --alluredir=report/report_json/
# 生成报告
#  allure serve report/report_json/
