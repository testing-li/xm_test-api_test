# -*- coding: utf-8 -*-
import pytest
import allure
from api.core.open_platform import open_project
from api.core.utils.api_yaml import _CONFIG

plat_config = _CONFIG['openplatform'][_CONFIG["env"]]


@allure.feature('open_project')
@allure.severity(allure.severity_level.NORMAL)
class TestOpenOraganization:
    apis = open_project.OpenPlatpormProject()

    # 获取项目列表
    @allure.title('获取项目列表')
    @pytest.mark.parametrize(('survey_id', "uid", "status", "start_udt", "end_udt", "page", "rowsPerPage", "re_title"),
                             [
                                 ("", None, "", "", "", 1, 10, None),
                                 ("", None, "", "", "", 1, 10, "test"),
                             ])
    def test_get_open_project_list(self, survey_id, uid, status, start_udt, end_udt, page, rowsPerPage,
                                   set_access_token, re_title):
        result = self.apis.get_open_project_list(survey_id, uid, status, start_udt, end_udt, page, rowsPerPage,
                                                 access_token=set_access_token, re_title=re_title)
        assert result['code'] == 0
        assert result['data']['total'] != 0
        data = result['data'].get('rows')
        if data:
            assert data[0].get('survey_name') is not None
            assert data[0].get('uid') is not None
            assert data[0].get('survey_id') is not None
            assert data[0].get('status') is not None
            assert data[0].get('fcount') is not None
            assert data[0].get('deliver_types') is not None
            assert f"{_CONFIG['base_url'][_CONFIG['env']]['openplatform_answer']}/s/{data[0].get('survey_id')}?source=1" in \
                   data[
                       0].get(
                       'preview_link')
            assert data[0].get(
                'edit_link') == f"{_CONFIG['base_url'][_CONFIG['env']]['openplatform']}/survey/edit/{data[0].get('survey_id')}/survey"
            assert data[0].get('response_link') is not None
            assert data[0].get('createDT') is not None
            assert data[0].get('updateDT') is not None

    @allure.title('错误获取项目列表')
    @pytest.mark.parametrize(('survey_id', "uid", "status", "start_udt", "end_udt", "page", "rowsPerPage"),
                             [
                                 ("1", "", None, "", "", 1, 10),
                                 (1, "", None, "", "", 1, 10),
                                 ("", "1", None, "", "", 1, 10),
                                 ("", 1, None, "", "", 1, 10),
                                 # ( "", "", -1, "", "", 1, 10),   空
                                 # ("", "", "test", "", "", 1, 10),  默认全部状态
                                 ("", "", None, "1", "", 1, 10),
                                 ("", "", None, 1, "", 1, 10),
                                 ("", "", None, "", 1, 1, 10),
                                 ("", "", None, "", "1", 1, 10),
                                 # ("", "", None, "", "", -1, 10),  -1时获取第一页
                                 # ("", "", None, "", "", "", 10),  为空默认1
                                 # ("", "", None, "", "", 1, -1),  -1默认获取10条
                                 # ("", "", None, "", "", 1, ""),  为空默认10
                                 # ("", "", None, "", "", 1, 99999)   所有数据
                             ])
    def test_get_open_project_list_fail(self, survey_id, uid, status, start_udt, end_udt, page, rowsPerPage,
                                        set_access_token):
        result = self.apis.get_open_project_list(survey_id, uid, status, start_udt, end_udt, page, rowsPerPage,
                                                 access_token=set_access_token)
        if isinstance(result, dict):
            assert result['code'] != 0
            assert result['code'] != -1
        else:
            assert result.json()['code'] != 0
            assert result.json()['code'] != -1

    # 问卷项目复制
    @allure.title('问卷项目复制')
    # @pytest.mark.skip("复制项目")
    @pytest.mark.parametrize(('title', 'survey_id'),
                             [
                                 ("项目复制", plat_config['default_survey_id'])
                             ])
    def test_post_open_copy_project(self, title, survey_id, set_access_token):
        result = self.apis.post_open_copy_project(title, survey_id, access_token=set_access_token)
        assert result['code'] == 0
        data = result['data']
        assert data.get('survey_name') == title
        assert data.get('uid') is not None
        assert data.get('survey_id') is not None
        assert data.get('status') is not None
        assert data.get('fcount') is not None
        assert data.get('deliver_types') is not None
        assert f"{_CONFIG['env']['openplatform_answer']}/s/{data.get('survey_id')}?source=1" in data.get('preview_link')
        assert data.get('edit_link') == f"{_CONFIG['env']['openplatform']}/survey/edit/{data.get('survey_id')}/survey"
        assert data.get('response_link') is not None
        assert data.get('createDT') is not None
        assert data.get('updateDT') is not None

    @allure.title('问卷项目复制异常')
    @pytest.mark.parametrize(('title', 'survey_id'),
                             [
                                 ("", plat_config['default_survey_id']),
                                 ("", ""),
                                 ("问卷复制", plat_config['org_id']),
                                 # (1, plat_config['default_survey_id']),  # 复制成功 字符转换
                                 ("问卷复制", 1),
                             ])
    def test_post_open_copy_project_fail(self, title, survey_id, set_access_token):
        result = self.apis.post_open_copy_project(title, survey_id, access_token=set_access_token)
        if isinstance(result, dict):
            assert result['code'] != 0
            assert result['code'] != -1
        else:
            assert result.json()['code'] != 0
            assert result.json()['code'] != -1

    # 答卷数据下载
    @allure.title('答卷数据下载')
    @pytest.mark.skip('下载')
    @pytest.mark.parametrize(('survey_id', 'ex_type', "call_back"),
                             [
                                 (plat_config['default_survey_id'], 0,
                                  'https://bvt.xm-test.bestcem.com/api/open/v1/callback/test/'),
                                 (plat_config['default_survey_id'], 1,
                                  'https://bvt.xm-test.bestcem.com/api/open/v1/callback/test/'),
                                 (plat_config['default_survey_id'], 2,
                                  'https://bvt.xm-test.bestcem.com/api/open/v1/callback/test/'),
                                 (plat_config['default_survey_id'], 3,
                                  'https://bvt.xm-test.bestcem.com/api/open/v1/callback/test/'),
                                 (plat_config['default_survey_id'], 5,
                                  'https://bvt.xm-test.bestcem.com/api/open/v1/callback/test/'),
                                 (plat_config['default_survey_id'], 6,
                                  'https://bvt.xm-test.bestcem.com/api/open/v1/callback/test/'),
                             ])
    def test_post_open_project_data_export(self, survey_id, ex_type, call_back, set_access_token):
        result = self.apis.post_open_project_data_export(survey_id, ex_type, call_back, access_token=set_access_token)
        assert result['code'] == 0
        data = result['data']
        assert data['msg'] == 'success'
        assert data.get('task_id') is not None

    @allure.title('答卷数据下载异常')
    @pytest.mark.parametrize(('survey_id', 'ex_type', "call_back"),
                             [
                                 #   callback不检验
                                 # (plat_config['default_survey_id'], 0, 'https://www.baidu.com'),
                                 (plat_config['org_id'], 0,
                                  'https://bvt.xm-test.bestcem.com/api/open/v1/callback/test/'),
                                 (plat_config['default_survey_id'], 0, ''),
                                 # (plat_config['default_survey_id'], -1,
                                 #  'https://bvt.xm-test.bestcem.com/api/open/v1/callback/test/'), 过期时间格式不对默认为0
                                 (plat_config['default_survey_id'], None,
                                  'https://bvt.xm-test.bestcem.com/api/open/v1/callback/test/'),
                                 # (plat_config['default_survey_id'], "1",
                                 #  'https://bvt.xm-test.bestcem.com/api/open/v1/callback/test/'), type可以是字符串
                                 (plat_config['default_survey_id'], None, 1),
                                 (1, 0, 'https://bvt.xm-test.bestcem.com/api/open/v1/callback/test/'),
                                 ("", 0, 'https://bvt.xm-test.bestcem.com/api/open/v1/callback/test/'),
                             ])
    def test_post_open_project_data_export_fail(self, survey_id, ex_type, call_back, set_access_token):
        result = self.apis.post_open_project_data_export(survey_id, ex_type, call_back, access_token=set_access_token)
        if isinstance(result, dict):
            assert result['code'] != 0
            assert result['code'] != -1
        else:
            assert result.json()['code'] != 0
            assert result.json()['code'] != -1

    # 创建问卷项目
    @allure.title('创建问卷项目')
    # @pytest.mark.skip('创建项目异常')
    @pytest.mark.parametrize(('qdes_title', 'project_title'),
                             [
                                 ("新建_问卷名称", "新建_项目名称"),
                                 ("新建_问卷名称1", ""),
                                 ("", "新建_项目名称2"),
                                 (None, "新建_项目名称3"),
                                 ("新建_问卷名称4", None)
                             ])
    def test_post_open_creat_project(self, qdes_title, project_title, set_access_token):
        result = self.apis.post_open_creat_project(qdes_title, project_title, access_token=set_access_token)
        assert result['code'] == 0
        data = result['data']
        assert data.get('id') is not None
        assert data.get("edit_url") == f"{_CONFIG['env']['openplatform']}/survey/edit/{data.get('id')}/survey"
        project_list = self.apis.get_open_project_list(data.get('id'), None, None, None, None, 1, 10, set_access_token)
        assert project_list['code'] == 0
        assert project_list['data'].get('rows')[0].get('survey_name') in (qdes_title, project_title)
        assert project_list['data'].get('rows')[0].get('survey_id') == data.get('id')

    # 修改问卷项目名称
    @allure.title('修改问卷、项目名称')
    # @pytest.mark.skip('创建项目异常')
    @pytest.mark.parametrize(('project_id', 'qdes_title', 'project_title'),
                             [
                                 (plat_config['default_survey_id'], "修改_问卷名称", "修改_项目名称"),
                                 (plat_config['default_survey_id'], "修改_问卷名称1", ""),
                                 (plat_config['default_survey_id'], "", "修改_项目名称2"),
                                 (plat_config['default_survey_id'], None, "修改_项目名称3"),
                                 (plat_config['default_survey_id'], "修改_问卷名称4", None),
                                 # (plat_config['default_survey_id'], "[示例]问卷调查项目", '[示例]问卷调查项目'),
                             ])
    def test_post_open_edit_project(self, project_id, qdes_title, project_title, set_access_token):
        result = self.apis.put_open_project_edit(project_id, qdes_title, project_title, access_token=set_access_token)
        assert result['code'] == 0
        data = result['data']
        assert data.get('id') == plat_config['default_survey_id']
        assert data.get("edit_url") == f"{_CONFIG['env']['openplatform']}/survey/edit/{data.get('id')}/survey"
        project_list = self.apis.get_open_project_list(data.get('id'), None, None, None, None, 1, 10, set_access_token)
        assert project_list['code'] == 0
        if qdes_title:
            assert project_list['data'].get('rows')[0].get('survey_name') == qdes_title
        else:
            assert project_list['data'].get('rows')[0].get('survey_name') is not None

    # 获取问卷最新版本的题目结构
    @allure.title('获取问卷最新版本的题目结构')
    @pytest.mark.parametrize(('project_id', "version"),
                             [
                                 (plat_config['default_survey_id'], 4),
                                 (plat_config['default_survey_id'], None),
                                 # ('60c07744aace70000b975014')
                             ])
    def test_get_open_project_struct_json(self, project_id, set_access_token, version):
        result = self.apis.get_open_project_struct_json(project_id, version, access_token=set_access_token)
        js_result = self.apis.get_project_js(project_id, version=version)
        assert result['code'] == 0
        data = js_result.json()["data"]
        data.setdefault("ucss", {})
        assert result['data'] == data

    # 获取问卷最新版本的题目结构异常case
    @allure.title('获取问卷最新版本的题目结构')
    @pytest.mark.parametrize(('project_id', "version"),
                             [
                                 (plat_config['default_survey_id'], 999),
                                 ("6rc07744aace70000b975014", 1),
                                 ("", 999999999999),
                                 (None, "1"),
                                 (plat_config['default_survey_id'], -1),
                                 (plat_config['default_survey_id'], "str"),
                                 # ('60c07744aace70000b975014')
                             ])
    def test_get_open_project_struct_json_error(self, project_id, set_access_token, version):
        result = self.apis.get_open_project_struct_json(project_id, version, access_token=set_access_token)
        if isinstance(result, dict):
            assert result['code'] != 0
            assert result['code'] != -1
        else:
            assert result.json()['code'] != 0
            assert result.json()['code'] != -1


    # 获取问卷gidmap
    @allure.title('获取问卷gidmap')
    @pytest.mark.parametrize(('project_id'),
                             [
                                 (plat_config['default_survey_id']),
                                 # ('60c2d98eaace70000b8b1c83')
                             ])
    def test_get_open_project_gidmap(self, project_id, set_access_token):
        result = self.apis.get_open_project_gidmap(project_id, access_token=set_access_token)
        assert result['code'] == 0
        assert result.get('data') is not None

    # 获取答卷数据统计
    @allure.title('获取答卷数据统计')
    @pytest.mark.parametrize(('project_ids'),
                             [
                                 [plat_config['default_survey_id'], '60c2d98eaace70000b8b1c83']
                             ])
    def test_get_open_project_summary(self, project_ids, set_access_token):
        result = self.apis.get_open_project_summary(project_ids, access_token=set_access_token)
        assert result['code'] == 0
        assert result['data']['total'] == len(project_ids)
        num = result['data']['rows'][0]['summary']
        assert num['count_all'] == num['count_doing'] + num['count_finish'] + num['count_unfinish'] + num[
            'count_screen_out'] + num['count_quota_full'] + num['count_backup']

    # 答卷数据导出json
    @allure.title('答卷数据导出json格式')
    @pytest.mark.parametrize(('survey_id', "page", "rowsPerPage", "start_time_gt", "start_time_lte", "finish_time_gt",
                              "finish_time_lte", "start_seq"),
                             [
                                 [plat_config['default_survey_id'], 1, 10, None, None, None, None, None],
                                 [plat_config['default_survey_id'], 1, 99999, None, None, None, None, None],
                                 [plat_config['default_survey_id'], 1, 10, "2021-04-01 00:00:00",
                                  None, None, None, None],
                                 [plat_config['default_survey_id'], 1, 10, None, "2021-04-01 23:59:59",
                                  None, None, None],
                                 [plat_config['default_survey_id'], 1, 10, None, None,
                                  "2021-04-01 00:00:00", None, None],
                                 [plat_config['default_survey_id'], 1, 10, None, None, None,
                                  "2021-04-01 23:59:59", None],
                                 [plat_config['default_survey_id'], 1, 10, "2021-04-01 00:00:00",
                                  "2021-04-01 23:59:59", None, None, None],
                                 [plat_config['default_survey_id'], 1, 10, None, None,
                                  "2021-04-01 00:00:00", "2021-04-01 23:59:59", None],
                                 [plat_config['default_survey_id'], 1, 10, "2021-04-01 00:00:00", None,
                                  None, "2021-04-01 23:59:59", None],
                                 [plat_config['default_survey_id'], 1, 10, None, None,
                                  None, None, "1"],
                             ])
    def test_get_answer_export_json(self, survey_id, page, rowsPerPage, start_time_gt: str, start_time_lte,
                                    finish_time_gt: str, finish_time_lte, start_seq, set_access_token):
        result = self.apis.get_open_qdes_export_json(survey_id, page, rowsPerPage,
                                                     start_time_gt, start_time_lte,
                                                     finish_time_gt, finish_time_lte, start_seq, set_access_token)
        assert result['code'] == 0
        assert result['data'].get('total') is not None
        assert result['data']['page_size'] <= rowsPerPage
        start_date = result['data']['rows'][0]['start']
        finish_date = result['data']['rows'][0].get("finish", "")
        if start_time_gt:
            assert start_date >= start_time_gt
        if start_time_lte:
            assert start_date <= start_time_lte
        if finish_time_gt:
            assert finish_date >= finish_time_gt
        if finish_time_lte:
            assert finish_date <= finish_time_lte

    @allure.title('环境清除')
    def test_clear_project(self, set_access_token):
        list = []
        with allure.step('获取项目列表'):
            project_list = self.apis.get_open_project_list(None, None, None, None, None, 1, 9999, set_access_token)
            assert project_list['code'] == 0
            data = project_list['data'].get('rows')
            for i in data:
                if i.get("survey_id") and i.get("survey_id") != plat_config['default_survey_id']:
                    list.append(i.get('survey_id'))
            assert list is not None
        with allure.step('删除默认项目外的其他项目'):
            delete_list = self.apis.delete_open_project_list(list, set_access_token)
            assert delete_list['code'] == 0
            delete_resule = self.apis.get_open_project_list(None, None, None, None, None, 1, 9999, set_access_token)
            assert delete_resule['code'] == 0
            delete_data = delete_resule['data'].get('rows')
            len = 0
            for i in delete_data:
                if i.get('status') != 3:
                    len += 1
            assert len == 1


if __name__ == '__main__':
    pytest.main(['./test_open_project.py'])
# 执行用例
# pytest -q -s tests/test_user/ --clean-alluredir --alluredir=report/report_json/
# 生成报告
#  allure serve report/report_json/
