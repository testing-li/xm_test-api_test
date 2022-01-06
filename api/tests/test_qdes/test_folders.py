#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import allure
from api.core.bestcem import folders
from api.utils.read_yaml import read_yaml


@allure.feature('folders')
@allure.severity(allure.severity_level.NORMAL)
class TestFloders:
    folder = folders.Folders()

    @allure.title('新增folders')
    @pytest.mark.parametrize(('par_name', 'child_name'),
                             read_yaml('/data/folders_tests_data.yml')['success'])
    def test_add_folders(self, par_name, child_name, set_headers):
        with allure.step('新增文件夹和子文件夹'):
            add = [{"name": par_name, "children": [{"name": child_name}], "projectCount": 0}]
            result = self.folder.put_folders(add, set_headers)
            assert result.json()['code'] == 0
        with allure.step('获取文件夹，确定添加结果'):
            result = self.folder.get_folders(set_headers)
            assert result.json()['data']['data']['folders'][0]['name'] == par_name
            assert result.json()['data']['data']['folders'][0]['children'][0]['name'] == child_name

    @allure.title('新增folders失败用例')
    @pytest.mark.parametrize(('par_name', 'child_name'),
                             read_yaml('/data/folders_tests_data.yml')['fail'])
    def test_add_folders_fail(self, par_name, child_name, set_headers):
        with allure.step('新增文件夹和子文件夹'):
            add = [{"name": par_name, "children": [{"name": child_name}], "projectCount": 0}]
            result = self.folder.put_folders(add, set_headers)
            assert result.json()['code'] != 0

    @allure.title('清除所有folders')
    def test_clear_folders(self, set_headers):
        with allure.step('获取文件夹列表'):
            get = self.folder.get_folders(set_headers)
        folders_list = get.json()['data']['data']['folders']
        assert get.json()['code'] == 0
        with allure.step('清除文件夹'):
            if len(folders_list) > 0:
                put = self.folder.put_folders(foldersList=[], token=set_headers)
                assert put.json()['code'] == 0
            else:
                pass


if __name__ == '__main__':
    pytest.main()
# 执行用例
# pytest -q -s tests/test_user/ --clean-alluredir --alluredir=report/report_json/
# 生成报告
#  allure serve report/report_json/
