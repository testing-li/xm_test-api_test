#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from api.core.utils import request
import requests
from api.utils import method
import random
import json
import threadpool
import re

base = {}
version = ''
structure_list = []
with open("../city", "r", encoding='utf-8') as f:
    city_info = eval(f.read())
"""
分页和分组的问卷答题时不一样的
"""


def re_short_url(url):
    """
    处理短链接
    :param url: 短链接
    :return: {location,baseurl,project_id,params}
    """
    global base
    base = {}
    r = request.get(url, env='')
    header = r.url
    match_obj = re.match(r'(http.*)/.*/(.*)\?(.*)', re.sub(r"signature", "sig", header), re.M | re.I)
    base['location'] = header
    base['baseurl'] = match_obj.group(1)
    base['project_id'] = match_obj.group(2)
    all_params = {}
    for i in match_obj.group(3).split('&'):
        line = i.split('=')
        all_params[line[0]] = line[1]
    base['all_params'] = all_params
    return base


def base_info(short_url):
    """
    长链接信息解析
    :param url: 答题链接
    :return: {version, structure_list}
    """
    d = {}
    re_shot = re_short_url(short_url)
    all_params = re_shot['all_params']
    source = re_shot['all_params']['source']
    base_url = re_shot['baseurl']
    project_id = re_shot['project_id']
    survey_url = f'{base_url}/api/survey/{project_id}?source={source}'
    js_url = request.post(url=survey_url, payload=all_params, env="").json()['data']["project_js"]
    if "http" not in js_url:
        js_url = f'{base_url}{js_url}'
    else:
        js_url = f'{js_url}'
    data = requests.get(js_url, params={"source": source}, verify=False).json()
    global structure_list
    structure_list = []
    if data['data']['customAttr'].get('openGrouping'):
        for i in data['data']['project']['items']:
            structure_list.append(i)  # 分组问卷
    else:
        for i in data['data']['project']['items']:
            if i.get("items"):
                structure_list += i['items']  # 分页问卷
    d['structure_list'] = structure_list
    global version
    version = data['data']['version']
    d['version'] = version
    return d


def blank_answer(blank_type, limit=None):
    """
    开放文本框类型判断
    :param blank_type: 开放文本框数据类型
    :param limit: 开放文本框限制（长度，日期格式）
    :return: 文本框答卷数据
    """
    num = 5
    if isinstance(limit, list) and blank_type not in ('number', "decimal"):
        num = method.range_int(limit)
    if blank_type in (0, "unlimit"):
        return "test"
    elif blank_type == 'email':
        return method.email()
    elif blank_type in ("mobile", "mobile_tel"):
        return method.phone()
    elif blank_type in ('number', "decimal"):
        if limit:
            min_num, max_num, digit = limit
            if not min_num:
                min_num = 0
            if not max_num:
                max_num = random.randint(int(min_num), 100)
            if not digit:
                digit = 2
            return str(round(random.uniform(float(min_num), float(max_num)), int(digit)))
        else:
            return str(round(random.uniform(0, 1), 2))
    elif blank_type == 'int':
        return str(num)
    elif blank_type == 'date':
        date_type = limit.upper()
        return method.getFormatTime(format=date_type)
    elif blank_type in ('lang_en', "en"):
        return method.lowercase(num)
    elif blank_type in ('lang_ch', "zh"):
        return method.chinese(num)
    elif blank_type == "idCard":
        return method.identity_number()
    elif blank_type == "tel":
        return method.tel_number()
    elif blank_type == "select":
        options = re.compile(r'\w+').findall(limit)
        return random.choice(options)
    else:
        return "test"


def cascade_answer(structure):
    """
    级联题目处理
    :param structure: 级联题问卷结构
    :return: 级联题答题数据
    """
    choose = {}
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    for i in range(len(structure)):
        if structure[i]['pid'] == '0_0':
            l1.append(i)
    c1 = random.choice(l1)
    for i in range(len(structure)):
        if structure[i]['pid'] == structure[c1]['ooid']:
            l2.append(i)
    if not l1:
        return {}
    choose['1'] = [structure[c1]['gid']]
    if not l2:
        return choose
    c2 = random.choice(l2)
    for i in range(len(structure)):
        if structure[i]['pid'] == structure[c2]['ooid']:
            l3.append(i)
    choose['2'] = [structure[c2]['gid']]
    if not l3:
        return choose
    c3 = random.choice(l3)
    for i in range(len(structure)):
        if structure[i]['pid'] == structure[c3]['ooid']:
            l4.append(i)
    choose['3'] = [structure[c3]['gid']]
    if not l4:
        return choose
    c4 = random.choice(l4)
    choose['4'] = [structure[c4]['gid']]
    return choose


def choose_city(content, level):
    """
    处理城市/地址题
    :param content: city.json文件
    :param level: 地址详细程度
    :return: dict ["1":province,"2":city, "3":district, "4":street]
    """
    choose = {}
    province = random.choice(content)
    city = random.choice(province['sub'])
    district = random.choice(city['sub'])
    street = method.street_address()
    data = [province['name'], city['name'], district['name'], street]
    for i in range(1, level + 1):
        choose[str(i)] = data[i - 1]
    return choose


def auto_table(content, line_num):
    """
    处理自增表格题数据
    :param content:  自增表格题
    :param line_num: 答题行数
    :return:
    """
    table = []
    items = content['items']
    for i in range(line_num):
        line = {}
        for j in items:
            gid = j["gid"]
            option_type = j['setType']
            option_value = j.get('setValue')
            value = blank_answer(option_type, option_value)
            line[str(gid)] = [value, ""]
        table.append(line)
    return table


def anal_questionnaire_structure(structure):
    d = {}
    if len(structure) == 0:
        return d
    for i in range(len(structure)):
        qtype = structure[i]['qtype']
        if qtype == 'single':  # 单选题
            if not structure[i].get('items'):
                continue
            title = str(structure[i]['gid'])
            choose_option = random.choice(structure[i]['items'])
            choose = [choose_option.get('gid')]
            if choose_option.get("is_open"):
                blank_type = choose_option['open_attrs'].get('type')
                long_range = choose_option['open_attrs'].get('range')
                choose.append(blank_answer(blank_type, long_range))
            d[title] = choose
        elif qtype == 'multiple':  # 多选题
            if not structure[i].get('items'):
                continue
            title = str(structure[i]['gid'])
            choose = []
            option_list = structure[i]['items']
            choose_list = random.sample(option_list, k=random.randrange(1, len(option_list) + 1))
            for j in choose_list:
                option = [j.get('gid')]
                if j.get("is_open"):
                    blank_type = j['open_attrs'].get('type')
                    long_range = j['open_attrs'].get('range')
                    option.append(blank_answer(blank_type, long_range))
                choose.append(option)
            d[title] = choose
        elif qtype == 'blank':  # 填空题
            title = str(structure[i]['gid'])
            blank_type = structure[i]['content_type']
            long_range = structure[i].get('words_number_range')
            d[title] = [blank_answer(blank_type, long_range)]
        elif qtype == 'multiple_blank':  # 多项填空题
            if not structure[i].get('items'):
                continue
            title = str(structure[i]['gid'])
            option = {}
            for j in range(len(structure[i]['items'])):
                gid = str(structure[i]['items'][j]['gid'])
                blank_type = structure[i]['items'][j]['open_attrs']['type']
                long_range = structure[i]['items'][j]['open_attrs'].get('range')
                option[gid] = [blank_answer(blank_type, long_range)]
            d[title] = option
        elif qtype == 'score' and structure[i]['custom_qtype'] != 'proportion':  # 打分题
            if not structure[i].get('items'):
                continue
            title = str(structure[i]['gid'])
            score_range = structure[i]['score_range']
            option = {}
            for j in structure[i]['items']:
                blank = ''
                if j.get("is_open"):
                    blank_type = j['open_attrs'].get('type')
                    long_range = j['open_attrs'].get('range')
                    blank = blank_answer(blank_type, long_range)
                option[str(j['gid'])] = [random.randrange(score_range[0], score_range[1] + 1), blank, ""]
            d[title] = option
        elif qtype == 'matrix_single':  # 矩阵单选
            if not structure[i].get('items') or not structure[i].get('rows_items'):
                continue
            q_gid = str(structure[i]['gid'])
            option = {}
            option_list = structure[i]['items']
            row_list = structure[i]['rows_items']
            for j in row_list:
                if j.get("is_open"):
                    blank_type = j['open_attrs'].get('type')
                    long_range = j['open_attrs'].get('range')
                    row_key = f"{str(j['gid'])}_open"
                    option[row_key] = blank_answer(blank_type, long_range)
                option_choose = random.choice(option_list)
                if option_choose.get("is_open"):
                    blank_type = j['open_attrs'].get('type')
                    long_range = j['open_attrs'].get('range')
                    option[str(j['gid'])] = [option_choose['gid'], blank_answer(blank_type, long_range)]
                else:
                    option[str(j['gid'])] = [option_choose['gid']]
            d[q_gid] = option
        elif qtype == 'matrix_multiple' and structure[i]['custom_qtype'] != 'classify':  # 矩阵多选
            if (not structure[i].get('items')) or (not structure[i].get('rows_items')):
                continue
            q_gid = str(structure[i]['gid'])
            option = {}
            option_list = structure[i]['items']
            row_list = structure[i]['rows_items']
            for j in row_list:
                if j.get("is_open"):
                    blank_type = j['open_attrs'].get('type')
                    long_range = j['open_attrs'].get('range')
                    row_key = f"{str(j['gid'])}_open"
                    option[row_key] = blank_answer(blank_type, long_range)
                option_choose = random.sample(option_list, k=random.randrange(1, len(option_list) + 1))
                row_answer = []
                for k in option_choose:
                    if not k.get("is_open"):
                        row_answer.append([k["gid"]])
                    else:
                        blank_type = k['open_attrs'].get('type')
                        long_range = k['open_attrs'].get('range')
                        row_answer.append([k['gid'], blank_answer(blank_type, long_range)])
                option[str(j["gid"])] = row_answer
            d[q_gid] = option
        elif qtype == 'matrix_blank':  # 矩阵填空
            if not structure[i].get('items') or not structure[i].get('rows_items'):
                continue
            q_gid = str(structure[i]['gid'])
            option = {}
            option_list = structure[i]['items']
            row_list = structure[i]['rows_items']
            for j in row_list:
                if j.get("is_open"):
                    blank_type = j['open_attrs'].get('type')
                    long_range = j['open_attrs'].get('range')
                    row_key = f"{str(j['gid'])}_open"
                    option[row_key] = blank_answer(blank_type, long_range)
                row_answer = {}
                for k in option_list:
                    blank_type = k['open_attrs'].get('type')
                    long_range = k['open_attrs'].get('range')
                    row_answer[str(k['gid'])] = blank_answer(blank_type, long_range)
                option[str(j["gid"])] = row_answer
            d[q_gid] = option
        elif qtype == 'matrix_score':  # 矩阵打分
            if not structure[i].get('items') or not structure[i].get('rows_items'):
                continue
            score_range = structure[i]['score_range']
            q_gid = str(structure[i]['gid'])
            option = {}
            option_list = structure[i]['items']
            row_list = structure[i]['rows_items']
            for j in row_list:
                if j.get("is_open"):
                    blank_type = j['open_attrs'].get('type')
                    long_range = j['open_attrs'].get('range')
                    row_key = f"{str(j['gid'])}_open"
                    option[row_key] = blank_answer(blank_type, long_range)
                row_answer = {}
                for k in option_list:
                    row_answer[str(k['gid'])] = random.randrange(score_range[0], score_range[1] + 1)
                option[str(j["gid"])] = row_answer
            d[q_gid] = option
        elif qtype == 'timedelta':  # 时间题
            title = str(structure[i]['gid'])
            d[title] = [method.hm_time()]
        elif qtype == 'timestamp':  # 日期题
            title = str(structure[i]['gid'])
            d[title] = [method.timestr(), 8]
        elif qtype == 'geo':  # 地理题
            coordinate = method.address_latlng()
            city = choose_city(city_info, 4)
            formatted_address = "".join(city.values())
            d1 = {"coordinate": coordinate,
                  "city": city,
                  "formattedAddress": formatted_address}
            title = str(structure[i]['gid'])
            d[title] = d1
        elif structure[i]['custom_qtype'] == 'proportion':  # 判断比重题
            d1 = {}
            title = str(structure[i]['gid'])
            total = structure[i]['total']
            lens = len(structure[i]['items'])
            fix_sum = method.fixSum(lens, total)
            for j in range(lens):
                gid = str(structure[i]['items'][j]['gid'])
                d1[gid] = fix_sum[j]
            d[title] = d1
        elif qtype == 'sort':  # 排序题
            if not structure[i].get('items'):
                continue
            d1 = {}
            title = str(structure[i]['gid'])
            choose = structure[i]['items']
            random.shuffle(choose)
            for j in range(len(choose)):
                if choose[j].get("is_open"):
                    blank_type = choose[j]['open_attrs'].get('type')
                    long_range = choose[j]['open_attrs'].get('range')
                    blank = blank_answer(blank_type, long_range)
                    d1[str(choose[j]['gid'])] = [j + 1, blank]
                else:
                    d1[str(choose[j]['gid'])] = j + 1
            d[title] = d1
        elif qtype == 'evaluation':  # 评价题
            d1 = {}
            title = str(structure[i]['gid'])
            lens = len(structure[i]['current_template']['scoreList'])
            score = random.randrange(lens)
            if structure[i]['current_template'].get("tagList", {}):
                content_gid = structure[i]['current_template']['scoreList'][score]['contentGid']
                d1["tagsId"] = random.sample(content_gid, k=random.randrange(0, len(content_gid) + 1))
            else:
                content = structure[i]['current_template']['scoreList'][score]['content'].split('\n')
                d1['tags'] = random.sample(content, k=random.randrange(0, len(content) + 1))
            d1['score'] = score + 1
            d1['open'] = "test"
            d[title] = d1
        elif qtype == 'city':  # 城市地址题
            title = str(structure[i]['gid'])
            level = structure[i]['info_level']
            choose = choose_city(city_info, level)
            d[title] = choose
        elif qtype == 'cascader':  # 级联题
            d1 = cascade_answer(structure[i]['option_list'])
            title = str(structure[i]['gid'])
            d[title] = d1
        elif structure[i]['custom_qtype'] == 'classify':  # 分类题
            choose = [[i['gid']] for i in structure[i]['items']]
            lens = len(structure[i]['rows_items'])
            cy = method.fixchoose(lens, choose)
            d1 = {}
            for j in range(lens):
                d1[str(structure[i]['rows_items'][j]['gid'])] = cy[j]
            title = str(structure[i]['gid'])
            d[title] = d1
        elif qtype == 'auto_table':  # 自增表格题
            title = str(structure[i]['gid'])
            content = structure[i]
            lens = int(structure[i]['defaultRows'])
            d[title] = auto_table(content, lens)
    return d


# 生成答卷数据
def creat_answer(url):
    if not structure_list:
        base_info(url)
    answer = anal_questionnaire_structure(structure_list)
    return answer


# 获取seq
def get_seq():
    data = {
        "allParams": base['all_params'],
        "source": base['all_params']['source'],
        "dev_id": ""
    }
    url = '{}/api/survey/b/{}/?source={}'.format(base['baseurl'], base['project_id'], base['all_params']['source'])
    r = request.post(url, data, env='')
    return r.json()['data']


def submit_answer(answer, seq_info):
    data = {
        "surveyId": base['project_id'],
        "version": version,
        "source": base['all_params']['source'],
        "code": base['all_params']['code'],
        "seq": seq_info['seq'],
        "status": 1,
        "data_status": 1,
        "allParams": base['all_params'],
        "answer": answer,
        "rspd_status": 1,
        "rspd_token": seq_info['jwt_token'],
        "uniq_qid_list": [],
    }
    header_ = {
        'Content-Type': 'application/json;charset=utf-8',
        "authorization": seq_info['jwt_token'],
        'user-agent': method.user_agent()
    }
    url = '{}/api/survey/s/{}/?source={}'.format(base['baseurl'], base['project_id'], base['all_params']['source'])
    r = request.post(url, headers=header_, payload=data, env='')
    return r


def submit_answer_by_data(answer, seq_info, ip, begin, finish):
    data = {
        "surveyId": base['project_id'],
        "version": version,
        "source": base['all_params']['source'],
        "code": base['all_params']['code'],
        "seq": seq_info['seq'],
        "status": 1,
        "data_status": 1,
        "allParams": base['all_params'],
        "answer": answer,
        "rspd_status": 1,
        "rspd_token": seq_info['jwt_token'],
        "uniq_qid_list": [],
        "s_begin_time": begin,
        "s_finish_time": finish
    }
    header_ = {
        "X-Forwarded-For": ip,
        'Content-Type': 'application/json;charset=utf-8',
        "authorization": seq_info['jwt_token'],
        'user-agent': method.user_agent()
    }
    url = '{}/api/survey/mock/s/{}/?source={}'.format(base['baseurl'], base['project_id'], base['all_params']['source'])
    r = request.post(url, headers=header_, payload=data, env='')
    return r


# 根据url答题
def auto_answer(url, num=1):
    for i in range(num):
        answer = json.dumps(creat_answer(url))
        # print(answer)
        seq = get_seq()
        # print(seq['seq'])
        submit_answer(answer, seq)


# 根据已有答卷数据答题
def answer_by_fix_data(answer, ip, begin, finish):
    seq = get_seq()
    submit_answer_by_data(answer, seq, ip, begin, finish)


def multi_answer(url, num=1, thread_num=8):
    """
    多线程答题，如果多份问卷答题需要修改creat_answer(url)方法，每次获取新的baseinfo
    :param url:
    :param num:
    :param thread_num:
    :return:
    """

    def answer_qdes(num):
        answer = json.dumps(creat_answer(url))
        seq = get_seq()
        submit_answer(answer, seq)

    num = [i for i in range(num)]
    pool = threadpool.ThreadPool(thread_num)
    requests = threadpool.makeRequests(answer_qdes, num)
    [pool.putRequest(req) for req in requests]
    pool.wait()


if __name__ == '__main__':
    t = time.perf_counter()
    # auto_answer("https://bestcem.com/t/557ORC", 1)
    multi_answer("https://bestcem.com/t/557ORC", 10)
    print(f'coast:{time.perf_counter() - t:.8f}s')
    # print(creatAnswer('https://bestcem.com/t/5553yH'))
