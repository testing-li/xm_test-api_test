#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import allure
from api.core.bestcem import folders, projects


@allure.feature('项目列表')
class TestProjects:
    folder = folders.Folders()
    qdes = projects.Projects()

    @allure.title('默认文件夹')
    @pytest.fixture(scope='module')
    @allure.severity(allure.severity_level.NORMAL)
    def default_folder(self, set_headers):
        add = [{"name": "test", "children": [], "projectCount": 0}]
        self.folder.put_folders(add, set_headers)
        folders_id = self.folder.get_folders(set_headers).json()['data']['data']['folders'][0]["id"]
        return folders_id

    @allure.title('默认项目')
    @pytest.fixture(scope='module')
    @allure.severity(allure.severity_level.NORMAL)
    def default_project(self, set_headers):
        project_list = self.qdes.get_project_list(token=set_headers)
        if project_list.json()['data']['total_count']:
            project_id = project_list.json()['data']['rows'][0]['project_id']
        else:
            project_id = self.qdes.post_creat_project('默认项目', '', set_headers).json()['data']['id']
        return project_id

    @allure.title('普通方式新建项目')
    @pytest.mark.parametrize(('title', "folder_id"), [
        ('普通创建项目', 'default'),
        ('未分组啊', '')
    ])
    def test_common_creat_project(self, title, folder_id, default_folder, set_headers):
        with allure.step('新增普通方式创建的项目'):
            if folder_id == 'default':
                result = self.qdes.post_creat_project(title, default_folder, set_headers)
            else:
                result = self.qdes.post_creat_project(title, folder_id, set_headers)
            assert result.json()['code'] == 0
            assert result.json()['data']['status'] == 0
        with allure.step('获取项目列表，确定添加结果'):
            project_list = self.qdes.get_project_list(token=set_headers)
            assert project_list.json()['code'] == 0
            assert project_list.json()['data']['rows'][0]['title'] == title

    @allure.title('普通方式新建项目错误')
    @pytest.mark.parametrize(('title', "folder_id"), [
        ('', '')
    ])
    def test_common_creat_project_fail(self, title, folder_id, set_headers):
        with allure.step('空的项目名和未知文件夹'):
            result = self.qdes.post_creat_project(title, folder_id, set_headers)
            assert result.json()['code'] != 0

    @allure.title('复制已有项目')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(("title", "folder_id"), [
        ('分组项目复制', 'default'),
        ('未分组复制项目', '')
    ])
    def test_copy_project(self, title, folder_id, default_project, default_folder, set_headers):
        with allure.step("获取已存在项目的ID"):
            project_id = default_project
        with allure.step('复制已有项目'):
            if folder_id == 'default':
                result = self.qdes.post_copy_project(project_id, title, default_folder, set_headers)
            else:
                result = self.qdes.post_copy_project(project_id, title, folder_id, set_headers)
            assert result.json()['code'] == 0
            assert result.json()['data']['status'] == 0
            assert result.json()['data']['title'] == title
        with allure.step('从列表查看添加结果'):
            pj_list = self.qdes.get_project_list(token=set_headers)
            assert pj_list.json()['code'] == 0
            assert pj_list.json()['data']['rows'][0]['title'] == title

    @allure.title('复制项目错误')
    @pytest.mark.parametrize(('project_id', 'title', "folder_id"), [
        ('6051c24caace70000c271111', '复制项目_01', ''),
        ('default', '', '')
    ])
    def test_copy_project_fail(self, project_id, title, folder_id, default_project, set_headers):
        with allure.step("获取已存在项目的ID"):
            pro_id = default_project
        with allure.step('空的项目名,位置项目'):
            if project_id == 'default':
                result = self.qdes.post_copy_project(pro_id, title, folder_id, set_headers)
            else:
                result = self.qdes.post_copy_project(project_id, title, folder_id, set_headers)
            assert result.json()['code'] != 0

    @allure.title('项目上传')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(('file'), [
        (('file', '../../data/file/export_demo_model.xls')),
    ])
    def test_import_project(self, file, set_headers):
        result = self.qdes.post_import_project(file, token=set_headers)
        assert result.json()['code'] == 0
        assert 'pid' in result.json()['data'].keys()
        assert 'sid' in result.json()['data'].keys()

    @allure.title('项目上传失败')
    @pytest.mark.parametrize(('file'), [
        (('files', '../../data/file/export_demo_model.xls')),
    ])
    def test_import_project_fail(self, file, set_headers):
        result = self.qdes.post_import_project(file, token=set_headers)
        assert result.json()['code'] != 0


if __name__ == '__main__':
    pytest.main(["./test_projects.py"])
