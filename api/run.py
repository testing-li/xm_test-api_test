# -*- coding: utf-8 -*-
import pytest
import os
import time
from api.utils import read_yaml
_config = read_yaml.read_yaml("/config.yaml")
"""
# 执行用例
pytest -q -s tests/test_user/ --clean-alluredir --alluredir=report/report_json/
# 生成报告
allure serve report/report_json/
"""
if __name__ == '__main__':
    pytest.main(['./tests/test_open_platform/test_open_user.py'])
    os.system("allure generate report/api_result_json/ -o report/report_result --clean")
    time.sleep(5)
    os.system(f'allure open -h {_config["report_address"]["ip"]} -p {_config["report_address"]["host"]} report/report_result/')
