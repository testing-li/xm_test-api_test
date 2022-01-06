#!/usr/bin/env python
# -*- coding: utf-8 -*-
from api.core.utils import request
from api.utils import method
import random
import re

base = {}
version = ''
structure_list = []
base_answer = ''
with open("city", "r", encoding='utf-8') as f:
    city_info = eval(f.read())
"""
自增表格题暂不支持
分页和分组的问卷答题时不一样的
"""


def reShotURL(url):
    global base
    base = {}
    r = request.get(url, env='')
    header = r.url
    matchObj = re.match(r'(http.*com)+?/.*/(.*)\?(.*)', re.sub(r"signature", "sig", header), re.M | re.I)
    base['location'] = header
    base['baseurl'] = matchObj.group(1)
    base['qnID'] = matchObj.group(2)
    allParams = {}
    for i in matchObj.group(3).split('&'):
        l = i.split('=')
        allParams[l[0]] = l[1]
    base['allParams'] = allParams
    return base


def baseinfo(url):
    d = {}
    reShot = reShotURL(url)
    source = reShot['allParams']['source']
    baseurl = reShot['baseurl']
    qnID = reShot['qnID']
    url = '{}/rs/survey/project/{}/project.js?source={}'.format(baseurl, qnID, source)
    data = request.get(url, env='').json()
    global structure_list
    structure_list = []
    if data['data']['customAttr'].get('openGrouping'):
        for i in data['data']['project']['items']:
            structure_list.append(i)  # 分组问卷
    else:
        for i in data['data']['project']['items']:
            if i.get("items"):
                structure_list += i['items']  # 分页问卷
    d['data'] = structure_list
    global version
    version = data['data']['version']
    d['version'] = version
    return d


# 解析一般题目（单选类型，多选类型，填空，多项填空，打分类型，日期，时间，地理，矩阵），返回字符串
def analData(rs):
    if len(rs) == 0:
        d = '{}'
    else:
        d = '{  '
    for i in range(len(rs)):
        if rs[i]['qtype'] == 'single':  # 判断单选题
            if not rs[i].get('items'):
                continue
            else:
                l1 = []
                title = str(rs[i]['gid'])
                for j in rs[i]['items']:
                    l2 = []
                    l2.append(j['gid'])
                    if "is_open" in j.keys() and j["is_open"] == True:
                        l2.append("test")
                    l1.append(l2)
                if i != len(rs) - 1:
                    d = d + '"{}": random.choice({})'.format(title, l1) + ', '
                else:
                    d = d + '"{}": random.choice({})'.format(title, l1) + '}'
        elif rs[i]['qtype'] == 'multiple':  # 判断多选题
            l1 = []
            title = str(rs[i]['gid'])
            for j in rs[i]['items']:
                l2 = []
                l2.append(j['gid'])
                if "is_open" in j.keys() and j["is_open"] == True:
                    l2.append(method.chinese(3))  # 这里没有判断输入框的输入类型
                l1.append(l2)
            if i != len(rs) - 1:
                d = d + '"{}": random.sample({},k=random.randrange({}, len({})+1))'.format(title, l1, 1, l1) + ', '
            else:
                d = d + '"{}": random.sample({},k=random.randrange({}, len({})+1))'.format(title, l1, 1, l1) + '}'
        elif rs[i]['qtype'] == 'blank':  # 判断填空题
            title = str(rs[i]['gid'])
            blank_type = rs[i]['content_type']
            long_range = rs[i].get('words_number_range')
            if i != len(rs) - 1:
                d = d + f'{title}: [method.type_choose("{blank_type}",{long_range})], '
            else:
                d = d + f'{title}: [method.type_choose("{blank_type}",{long_range})]}}'
        elif rs[i]['qtype'] == 'multiple_blank':  # 判断多项填空题
            title = str(rs[i]['gid'])
            sub_char = '{'
            for j in range(len(rs[i]['items'])):
                gid = str(rs[i]['items'][j]['gid'])
                blank_type = rs[i]['items'][j]['open_attrs']['type']
                long_range = rs[i]['items'][j]['open_attrs'].get('range')
                if j != len(rs[i]['items']) - 1:
                    sub_char = sub_char + f'"{gid}": [method.type_choose("{blank_type}",{long_range})], '
                else:
                    sub_char = sub_char + f'"{gid}": [method.type_choose("{blank_type}",{long_range})]}}'
            if i != len(rs) - 1:
                d = d + '"{}": {}'.format(title, sub_char) + ', '
            else:
                d = d + '"{}": {}'.format(title, sub_char) + '}'
        elif rs[i]['qtype'] == 'score' and rs[i]['custom_qtype'] != 'proportion':  # 判断打分题
            title = str(rs[i]['gid'])
            score_range = rs[i]['score_range']
            sub_char = '{'
            for j in range(len(rs[i]['items'])):
                gid = str(rs[i]['items'][j]['gid'])
                if j != len(rs[i]['items']) - 1:
                    sub_char = sub_char + '"{}": [random.randrange({}, {}),"",""]'.format(gid, score_range[0],
                                                                                          score_range[
                                                                                              1] + 1) + ', '  # 打分题填空框未处理
                else:
                    sub_char = sub_char + '"{}": [random.randrange({}, {}),"",""]'.format(gid, score_range[0],
                                                                                          score_range[1] + 1) + '}'
            if i != len(rs) - 1:
                d = d + '"{}": {}'.format(title, sub_char) + ', '
            else:
                d = d + '"{}": {}'.format(title, sub_char) + '}'
        elif rs[i]['qtype'] == 'matrix_single':  # 判断矩阵单选
            title = str(rs[i]['gid'])
            c_title = []
            c_choose = []
            sub_char = '{'
            for j in rs[i]['items']:
                c_choose.append(j['gid'])
            for j in rs[i]['rows_items']:
                c_title.append(str(j['gid']))
            for j in range(len(c_title)):
                if j != len(c_title) - 1:
                    sub_char = sub_char + '"{}": [random.choice({})]'.format(c_title[j], c_choose) + ', '
                else:
                    sub_char = sub_char + '"{}": [random.choice({})]'.format(c_title[j], c_choose) + '}'
            if i != len(rs) - 1:
                d = d + '"{}": {}'.format(title, sub_char) + ', '
            else:
                d = d + '"{}": {}'.format(title, sub_char) + '}'
        elif rs[i]['qtype'] == 'matrix_multiple' and rs[i]['custom_qtype'] != 'classify':  # 判断矩阵多选
            title = str(rs[i]['gid'])
            c_title = []
            c_choose = []
            sub_char = '{'
            for j in rs[i]['items']:
                c_choose.append([(j['gid'])])
            for j in rs[i]['rows_items']:
                c_title.append(str(j['gid']))
            for j in range(len(c_title)):
                if j != len(c_title) - 1:
                    sub_char = sub_char + \
                               '"{}": random.sample({},k=random.randrange({}, len({})+1))' \
                                   .format(c_title[j], c_choose, 1, c_choose) + ', '
                else:
                    sub_char = sub_char + \
                               '"{}": random.sample({},k=random.randrange({}, len({})+1))' \
                                   .format(c_title[j], c_choose, 1, c_choose) + '}'
            if i != len(rs) - 1:
                d = d + '"{}": {}'.format(title, sub_char) + ', '
            else:
                d = d + '"{}": {}'.format(title, sub_char) + '}'
        elif rs[i]['qtype'] == 'matrix_blank':  # 判断矩阵填空
            title = str(rs[i]['gid'])
            c_title = []
            c_choose = []
            sub_char = '{'
            for j in rs[i]['items']:
                c_choose.append((str(j['gid'])))
            for j in rs[i]['rows_items']:
                c_title.append(str(j['gid']))
            for j in range(len(c_title)):
                sub_char2 = '{'
                for k in range(len(c_choose)):
                    if k != len(c_choose) - 1:
                        sub_char2 = sub_char2 + '"{}": method.chinese(3)'.format(c_choose[k]) + ', '
                    else:
                        sub_char2 = sub_char2 + '"{}": method.chinese(3)'.format(c_choose[k]) + '}'
                if j != len(c_title) - 1:
                    sub_char = sub_char + '"{}": {}'.format(c_title[j], sub_char2) + ', '
                else:
                    sub_char = sub_char + '"{}": {}'.format(c_title[j], sub_char2) + '}'
            if i != len(rs) - 1:
                d = d + '"{}": {}'.format(title, sub_char) + ', '
            else:
                d = d + '"{}": {}'.format(title, sub_char) + '}'
        elif rs[i]['qtype'] == 'matrix_score':  # 判断矩阵打分
            title = str(rs[i]['gid'])
            score_range = rs[i]['score_range']
            c_title = []
            c_choose = []
            sub_char = '{'
            for j in rs[i]['items']:
                c_choose.append((str(j['gid'])))
            for j in rs[i]['rows_items']:
                c_title.append(str(j['gid']))
            for j in range(len(c_title)):
                sub_char2 = '{'
                for k in range(len(c_choose)):
                    if k != len(c_choose) - 1:
                        sub_char2 = sub_char2 + '"{}": random.randrange({}, {})'.format(c_choose[k], score_range[0],
                                                                                        score_range[1] + 1) + ', '
                    else:
                        sub_char2 = sub_char2 + '"{}": random.randrange({}, {})'.format(c_choose[k], score_range[0],
                                                                                        score_range[1] + 1) + '}'
                if j != len(c_title) - 1:
                    sub_char = sub_char + '"{}": {}'.format(c_title[j], sub_char2) + ', '
                else:
                    sub_char = sub_char + '"{}": {}'.format(c_title[j], sub_char2) + '}'
            if i != len(rs) - 1:
                d = d + '"{}": {}'.format(title, sub_char) + ', '
            else:
                d = d + '"{}": {}'.format(title, sub_char) + '}'
        elif rs[i]['qtype'] == 'timedelta':  # 判断矩阵打分
            title = str(rs[i]['gid'])
            if i != len(rs) - 1:
                d = d + '"{}": [method.hm_time()]'.format(title) + ', '
            else:
                d = d + '"{}": [method.hm_time()]'.format(title) + '}'
        elif rs[i]['qtype'] == 'timedelta':  # 判断时间题
            title = str(rs[i]['gid'])
            if i != len(rs) - 1:
                d = d + '"{}": [method.hm_time()]'.format(title) + ', '
            else:
                d = d + '"{}": [method.hm_time()]'.format(title) + '}'
        elif rs[i]['qtype'] == 'timestamp':  # 判断日期题
            title = str(rs[i]['gid'])
            if i != len(rs) - 1:
                d = d + '"{}": [method.timestr(),8]'.format(title) + ', '
            else:
                d = d + '"{}": [method.timestr(),8]'.format(title) + '}'
        elif rs[i]['qtype'] == 'geo':  # 地理题 写死
            d1 = {"coordinate": [121.475391, 31.232767], "city": {"1": "上海市", "2": "上海市", "3": "黄浦区", "4": "南京东路街道"},
                  "formattedAddress": "上海市黄浦区南京东路街道西藏中路195号人民公园"}
            title = str(rs[i]['gid'])
            if i != len(rs) - 1:
                d = d + '"{}": {}'.format(title, d1) + ', '
            else:
                d = d + '"{}": {}'.format(title, d1) + '}'
    d = list(d)
    if d[-1] != '}':
        d.pop()
        d[-1] = '}'
    d = ''.join(d)
    global base_answer
    base_answer = d
    return d


# 处理级联题数据
def cascader(l):
    d = {}
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    for i in range(len(l)):
        if l[i]['pid'] == '0_0':
            l1.append(i)
    c1 = random.choice(l1)
    for i in range(len(l)):
        if l[i]['pid'] == l[c1]['ooid']:
            l2.append(i)
    if l2 == []:
        d['1'] = [l[c1]['gid']]
        return d
    c2 = random.choice(l2)
    for i in range(len(l)):
        if l[i]['pid'] == l[c2]['ooid']:
            l3.append(i)
    if l3 == []:
        d['1'] = [l[c1]['gid']]
        d['2'] = [l[c2]['gid']]
        return d
    c3 = random.choice(l3)
    for i in range(len(l)):
        if l[i]['pid'] == l[c3]['ooid']:
            l4.append(i)
    if l4 == []:
        d['1'] = [l[c1]['gid']]
        d['2'] = [l[c2]['gid']]
        d['3'] = [l[c3]['gid']]
        return d
    c4 = random.choice(l4)
    d['1'] = [l[c1]['gid']]
    d['2'] = [l[c2]['gid']]
    d['3'] = [l[c3]['gid']]
    d['4'] = [l[c4]['gid']]
    return d


# 处理城市/地址题
def choose_city(content, level):
    choose = {}
    province = random.choice(content)
    city = random.choice(province['sub'])
    district = random.choice(city['sub'])
    street = "test"
    l = [province['name'], city['name'], district['name'], street]
    for i in range(1, level + 1):
        choose[str(i)] = l[i - 1]
    return choose


# 处理自增表格题数据
def auto_table(content, len):
    table = []
    items = content['items']
    for j in range(len):
        line = {}
        for i in items:
            gid = i["gid"]
            type = i['setType']
            value = ""
            if type == "int":
                value = method.strNum(2)
            elif type == "unlimit":
                value = "test"
            elif type == "select":
                options = re.compile(r'\w+').findall(i["setValue"])
                value = random.choice(options)
            elif type == "email":
                value = method.email()
            elif type == "mobile":
                value = method.phone()
            line[str(gid)] = [value, ""]
        table.append(line)
    return table


# 判断比重题 排序题 评价题 地理位置题 级联题(自定义和行业题) 分类题 自增表格题
def ana(d):
    for i in range(len(structure_list)):
        if structure_list[i]['custom_qtype'] == 'proportion':  # 判断比重题
            d1 = {}
            title = str(structure_list[i]['gid'])
            total = structure_list[i]['total']
            lens = len(structure_list[i]['items'])
            l = method.fixSum(lens, total)
            for j in range(lens):
                gid = str(structure_list[i]['items'][j]['gid'])
                d1[gid] = l[j]
            d[title] = d1
        elif structure_list[i]['qtype'] == 'sort':  # 排序题
            d1 = {}
            title = str(structure_list[i]['gid'])
            choose = [i['gid'] for i in structure_list[i]['items']]
            random.shuffle(choose)
            for j in range(len(choose)):
                d1[str(choose[j])] = j + 1
            d[title] = d1
        elif structure_list[i]['qtype'] == 'evaluation':  # 评价题
            d1 = {}
            title = str(structure_list[i]['gid'])
            lens = len(structure_list[i]['current_template']['scoreList'])
            score = random.randrange(lens)
            content = structure_list[i]['current_template']['scoreList'][score]['content'].split('\n')
            d1['score'] = score + 1
            d1['open'] = method.chinese(3)
            d1['tags'] = random.sample(content, k=random.randrange(0, len(content) + 1))
            d[title] = d1
        elif structure_list[i]['qtype'] == 'city':  # 地理位置题 写死
            title = str(structure_list[i]['gid'])
            level = structure_list[i]['info_level']
            choose = choose_city(city_info, level)
            d[title] = choose
        elif structure_list[i]['qtype'] == 'cascader':  # 级联题
            d1 = cascader(structure_list[i]['option_list'])
            title = str(structure_list[i]['gid'])
            d[title] = d1
        elif structure_list[i]['custom_qtype'] == 'classify':  # 分类题
            choose = [[i['gid']] for i in structure_list[i]['items']]
            lens = len(structure_list[i]['rows_items'])
            cy = method.fixchoose(lens, choose)
            d1 = {}
            for j in range(lens):
                d1[str(structure_list[i]['rows_items'][j]['gid'])] = cy[j]
            title = str(structure_list[i]['gid'])
            d[title] = d1
        elif structure_list[i]['qtype'] == 'auto_table':  # 自增表格题
            title = str(structure_list[i]['gid'])
            content = structure_list[i]
            lens = int(structure_list[i]['defaultRows'])
            d[title] = auto_table(content, lens)
    return d


# 生成答卷数据
def creatAnswer(url):
    if structure_list == []:
        baseinfo(url)
    if base_answer == '':
        analData(structure_list)
    d1 = eval(base_answer)
    answer = ana(d1)
    return answer


# 获取seq
def getSeq():
    source = base['allParams']['source']
    baseurl = base['baseurl']
    qnID = base['qnID']
    allParams = base['allParams']
    data = {
        "allParams": allParams,
        "source": source,
        "dev_id": ""
    }
    url = '{}/api/survey/b/{}/?source={}'.format(baseurl, qnID, source)
    r = request.post(url, data, env='')
    return r.json()['data']


def answerWenjuan(content, seq_info):
    answer = content
    data = {
        "surveyId": base['qnID'],
        "version": version,
        "source": base['allParams']['source'],
        "code": base['allParams']['code'],
        "seq": seq_info['seq'],
        "status": 1,
        "data_status": 1,
        "allParams": base['allParams'],
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
    url = '{}/api/survey/s/{}/?source={}'.format(base['baseurl'], base['qnID'], base['allParams']['source'])
    r = request.post(url, headers=header_, payload=data, env='')
    return r


def answerWenjuan_by_data(content, seq_info, ip, begin, finish):
    answer = content
    data = {
        "surveyId": base['qnID'],
        "version": version,
        "source": base['allParams']['source'],
        "code": base['allParams']['code'],
        "seq": seq_info['seq'],
        "status": 1,
        "data_status": 1,
        "allParams": base['allParams'],
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
    url = '{}/api/survey/mock/s/{}/?source={}'.format(base['baseurl'], base['qnID'], base['allParams']['source'])
    r = request.post(url, headers=header_, payload=data, env='')
    return r


# 根据url答题
def autoAnswer(url, num=1):
    for i in range(num):
        answer = creatAnswer(url)
        print(answer)
        seq = getSeq()
        # print(seq['seq'])
        answerWenjuan(answer, seq)


def answer_by_fix_data(answer, ip, begin, finish):
    seq = getSeq()
    answerWenjuan_by_data(answer, seq, ip, begin, finish)


if __name__ == '__main__':
    import time
    t = time.perf_counter()
    autoAnswer('https://bestcem.com/t/55502R', 1)
    print(f'coast:{time.perf_counter() - t:.8f}s')
    # baseinfo('https://bestcem.com/t/5RhXip')
    # for i in range(1):
    #     import time
    #
    #     time.sleep(2)
    #     autoAnswer('https://bestcem.com/t/555EJP', 1)
