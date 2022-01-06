import requests
import hashlib
import re
import json
import urllib3
import jsonpath
from collections import Counter


class ZentaoClient(object):
    session = None  # 用于实现单例类，避免多次申请sessionID

    def __init__(self, url, account, password, productID=22):
        self.url = url
        self.account = account  # 账号
        self.password = password  # 密码
        self.productID = productID  # 禅道bug项目ID
        self.pages = {
            # 登录的接口
            "login": f"{self.url}/user-login.json",
            # 创建筛选条件
            "search": f"{self.url}/search-buildQuery.json",
            # 获取结果数据
            "actionURL": f"{self.url}/bug-browse-{self.productID}-0-bySearch-myQueryID.json",
            # 用户列表信息
            "user_list": f"{self.url}/company-browse.json"
        }
        self.s = None

    def login(self):
        if not self.s:
            urllib3.disable_warnings()
            self.s = requests.session()
            data = self.s.get(self.pages['login'], verify=False).json()['data']
            verify = json.loads(data)['rand']
            # 第一次加密密码
            pwd1md5 = hashlib.md5()
            pwd1md5.update(self.password.encode('utf-8'))
            pwd1_result = pwd1md5.hexdigest()
            # 第2次加密
            pwd2md5 = hashlib.md5()
            pwd2md5.update((pwd1_result + str(verify)).encode('utf-8'))
            pwd2_result = pwd2md5.hexdigest()
            body = {
                "account": self.account,
                "password": pwd2_result,
                "passwordStrength": 1,
                "referer": "/",
                "verifyRand": verify,
                "keepLogin": 0,
            }
            # 登录请求
            login_data = self.s.post(self.pages['login'], data=body).json()
            if login_data.get('status') == 'success':
                print('登录成功！！')
                ZentaoClient.session = self.s
            else:
                print('登录失败！！')
                exit(0)

    def get_user_list(self, type=0):
        """
        获取禅道用户映射字典
        :return: dict
        :param: type: 0 所有 1开发 2产品
        """
        d = {}
        user_list_url = self.pages["user_list"]
        # 自定义cookies，设置禅道列表页面的条数
        cookies = {'pagerCompanyBrowse': '1000'}
        data = self.s.get(user_list_url, cookies=cookies, verify=False)
        resp = data.json()['data']
        users = json.loads(resp)['users']
        dev_users = [i['account'] for i in users if i['role'] in ['dev', '']]
        d['dev_users'] = dev_users
        for i in users:
            d[i['realname']] = i['account']
        return d

    def search_result(self, date='', status='', name=''):
        """
        通过单个时间和bug状态搜索答卷数据
        :param date:"$lastWeek","thisWeek","lastMonth","thisMonth"
        :param status: "active","resolved","closed"
        :return:
        """
        search_url = self.pages["search"]
        result_url = self.pages["actionURL"]
        search_form_data = {
            "fieldproduct": self.productID,
            "andOr1": "AND",
            "field1": "assignedTo",
            "operator1": "=",
            "value1": name,
            "andOr2": "or",
            "field2": "resolvedBy",
            "operator2": "=",
            "value2": name,
            "andOr3": "and",
            "field3": "openedDate",
            "operator3": "between",
            "value3": date,
            "andOr4": "AND",
            "field4": "status",
            "operator4": "=",
            "value4": status,
            "module": "bug"
        }
        self.s.post(search_url, data=search_form_data, verify=False)
        # 自定义cookies，设置产业列表页面的条数
        cookies = {'lastProduct': f'{self.productID}',
                   'preProductID': f'{self.productID}', 'qaBugOrder': 'id_desc', 'theme': 'default',
                   'pagerBugBrowse': '1000'}
        web = self.s.get(result_url, cookies=cookies, verify=False)
        resp = web.json()['data']
        s = json.loads(resp)
        return s

    def bug_screen(self, content):
        """
        开发有效bug
        :param content:
        :return:
        """
        bugs_list = content['bugs']
        dev_users = self.get_user_list()['dev_users']
        screen_bug_list = []
        for i in range(len(bugs_list)):
            if bugs_list[i]["resolution"] not in ["duplicate", "bydesign", "notrepro"] and \
                    (bugs_list[i]['type'] not in ["designdefect", "designchange"]):
                if bugs_list[i]["status"] == "active":
                    if bugs_list[i]['assignedTo'] in dev_users:
                        screen_bug_list.append(bugs_list[i])
                else:
                    if bugs_list[i]['resolvedBy'] in dev_users:
                        screen_bug_list.append(bugs_list[i])
        content["bugs"] = screen_bug_list
        return content

    def bug_environment_classify(self, content):
        """
        content 内容加上环境分类
        :param content:
        :return:
        """
        master_bugs = []
        other_bugs = []
        pattern = "线上"
        for i in content["bugs"]:
            if re.search(pattern, i['title']):
                master_bugs.append(i)
            else:
                other_bugs.append(i)
        content["master_bugs"] = {"bugs": master_bugs}
        content["other_bugs"] = {"bugs": other_bugs}
        return content

    def bug_count_classify(self, content):
        """
        对bug列表数据按用户名进行归类统计
        :param content: 禅道页面json源数据
        :return:
        """
        data = {}
        data["num"] = len(content["bugs"])
        data["active_num"] = 0 if not jsonpath.jsonpath(content, "$.bugs[*].status") \
            else jsonpath.jsonpath(content, "$.bugs[*].status").count('active')
        data["solve_num"] = data["num"] - data["active_num"]
        data["active_bug"] = {} if not data["active_num"] else jsonpath.jsonpath(content,
                                                                                 "$.bugs[?(@.status == 'active')]")
        data["solve_bug"] = {} if not data["solve_num"] else jsonpath.jsonpath(content,
                                                                               "$.bugs[?(@.status != 'active')]")
        # bug按状态和级别统计名单
        lt_error_active_name = jsonpath.jsonpath(data, "$.active_bug[?(@.severity>'2')].assignedTo")
        gte_error_active_name = jsonpath.jsonpath(data, "$.active_bug[?(@.severity<'3')].assignedTo")
        lt_error_solve_name = jsonpath.jsonpath(data, "$.solve_bug[?(@.severity>'2')].resolvedBy")
        gte_error_solve_name = jsonpath.jsonpath(data, "$.solve_bug[?(@.severity<'3')].resolvedBy")
        lt_error_active = {} if not lt_error_active_name else dict(Counter(lt_error_active_name))
        gte_error_active = {} if not gte_error_active_name else dict(Counter(gte_error_active_name))
        lt_error_solve = {} if not lt_error_solve_name else dict(Counter(lt_error_solve_name))
        gte_error_solve = {} if not gte_error_solve_name else dict(Counter(gte_error_solve_name))
        lt_error_data = dict(Counter(lt_error_active) + Counter(lt_error_solve))
        gte_error_data = dict(Counter(gte_error_active) + Counter(gte_error_solve))
        # 按bug状态统计单名
        active_name = jsonpath.jsonpath(data, "$.active_bug[*].assignedTo")
        solve_name = jsonpath.jsonpath(data, "$.solve_bug[*].resolvedBy")
        data["active_name"] = {} if not active_name else dict(Counter(active_name))
        data["solve_name"] = {} if not solve_name else dict(Counter(solve_name))
        data["total_name"] = dict(Counter(data["active_name"]) + Counter(data["solve_name"]))
        data["lt_name"] = lt_error_data
        data["gte_name"] = gte_error_data
        return data

    def bug_dever_count(self, content):
        all = self.bug_count_classify(content)
        other = self.bug_count_classify(content['other_bugs'])
        master = self.bug_count_classify(content['master_bugs'])
        data = {}
        data["total_num"] = all["num"]
        data["total_active_num"] = all["active_num"]
        data["total_solve_num"] = all["solve_num"]
        data["master_num"] = master["num"]
        data["master_active_num"] = master["active_num"]
        data["master_solve_num"] = master["solve_num"]
        rows = []
        for key, value in all["total_name"].items():
            row = {}
            # 获取禅道用户列表
            row["name"] = content['users'].get(key, key)
            row['active'] = all["active_name"].get(key, 0)
            row['solve'] = all["solve_name"].get(key, 0)
            row['total'] = value
            row['other_lt_error'] = other["lt_name"].get(key, 0)
            row['other_gte_error'] = other["gte_name"].get(key, 0)
            row['master_lt_error'] = master["lt_name"].get(key, 0)
            row['master_gte_error'] = master["gte_name"].get(key, 0)
            rows.append(row)
        data["rows"] = rows
        return data

    def count_tester_bugs(self, content):
        """
        对bug列表创建者用户名归类统计
        :param content: 禅道页面json源数据
        :return:
        """
        master_content = content.get("master_bugs", 0)
        bug_openby_data = jsonpath.jsonpath(master_content, "$.bugs[*].openedBy")
        open_by = {} if not bug_openby_data else dict(Counter(bug_openby_data))
        gte_error_data = jsonpath.jsonpath(master_content, "$.bugs[?(@.severity<'3')].openedBy")
        gte_error = {} if not gte_error_data else dict(Counter(gte_error_data))
        lt_error_data = jsonpath.jsonpath(master_content, "$.bugs[?(@.severity>'2')].openedBy")
        lt_error = {} if not lt_error_data else dict(Counter(lt_error_data))
        rows = []
        for key, value in open_by.items():
            row = {}
            # 获取禅道用户列表
            row["name"] = content['users'].get(key, key)
            row['lt_error'] = lt_error.get(key, 0)
            row['gte_error'] = gte_error.get(key, 0)
            rows.append(row)
        return rows


if __name__ == '__main__':
    s = ZentaoClient("https://zentao.idiaoyan.cn", account="xx.zong", password="Zxx1234")
    s.login()
    # s.get_user_list()
    bugs = s.search_result(date="lastMonth")
    # print(bugs['bugs'])
    # s.bug_screen(bugs)
    print(s.count_tester_bugs(bugs))
    # cy = s.bug_classify(bugs)
    # print(cy["master_bugs"])
    # # print(len(cy["master_bugs"]))
    # print(s.get_user_list())
