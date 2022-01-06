#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import arrow
from faker import Factory
import os
import time
import logging

"""
创建测试数据方法
"""
f = Factory().create('zh-CN')


def mkdir(dir_path):
    """ 创建路径
    """
    # 去除首位空格
    _dir = dir_path.strip()
    _dir = dir_path.rstrip("\\")
    _dir = dir_path.rstrip("/")

    # 判断路径是否存在
    is_exists = os.path.exists(_dir)

    if not is_exists:
        try:
            os.makedirs(_dir)
        except Exception as e:
            logging.error("Directory creation failed：%s" % e)
    else:
        # 如果目录存在则不创建，并提示目录已存在
        logging.debug("Directory already exists：%s" % str(_dir))


# 随机取任意长度数字字符
def strNum(len=1):
    text = '1234567890'
    text_new = (''.join(random.choice(text) for i in range(len)))
    return text_new


# 随机获取任意长度数字
def long_num(lenth=1):
    text = '1234567890'
    num = (''.join(random.choice(text) for i in range(lenth)))
    return int(num)


# 获取范围内整数
def range_num(min, max):
    return random.randint(min, max)


# 随机取任意数量字符
def Uppercase(number=1):
    text = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text_new = (''.join(random.choice(text) for i in range(number)))
    return text_new


# 随机取任意数量字符
def lowercase(number=1):
    text = 'abcdefghijklmnopqrstuvwxyz'
    text_new = (''.join(random.choice(text) for i in range(number)))
    return text_new


# 随机取任意数量字符
def chinese(number=1):
    text = '离离原上草，一岁一枯荣。野火烧不尽，春风吹又生。远芳侵古道，晴翠接荒城。又送王孙去，萋萋满别情。人间四月芳菲尽，山寺桃花始盛开。长恨春归无觅处，不知转入此中来。天长地久有时尽，此恨绵绵无绝期。在天愿作比翼鸟，在地愿为连理枝。' \
           '别有幽愁暗恨生，此时无声胜有声。同是天涯沦落人，相逢何必曾相识。细草微风岸，危樯独夜舟。星垂平野阔，月涌大江流。名岂文章著，官应老病休。飘飘何所似？天地一沙鸥。'
    text_new = (''.join(random.choice(text) for i in range(number)))
    return text_new


# 随机取任意数量字符 （缺'_'）
def half_angle(number=1):
    text = r'~`!@#$%^&*()-+={[}]|\:;"<.,>?/'
    text_new = (''.join(random.choice(text) for i in range(number)))
    return text_new


# 符号字符
def full_symbol(number=1):
    text = r'`~！#￥%……&*（）——-+={【}】|、《，》。？、：；"'
    text_new = (''.join(random.choice(text) for i in range(number)))
    return text_new


# 随机取任意数量字符，但是绘文字在前端中算2个字符
def emoji(number=1):
    text = '👌💋🚗🍰🐱🐶🐭🎁🎂'
    text_new = (''.join(random.choice(text) for i in range(number)))
    return text_new


# 随机取任意数量字符
def japanese(number=1):
    text = 'にほんごなくてないで'
    text_new = (''.join(random.choice(text) for i in range(number)))
    return text_new


# 随机取任意数量字符
def Arabic(number=1):
    text = "خلف سوق الذه"
    text_new = (''.join(random.choice(text) for i in range(number)))
    return text_new


# 除数字下划线字母以为的字符组合
def numberTitle(chi=1, japen=1, fullSymbol=1, halfSy=1):
    text = chinese(chi) + japanese(japen) + full_symbol(fullSymbol) + half_angle(halfSy)
    return text


# 把所有常用类型的字符拼接在了一起，默认都取一个字符
def usu_text(lower=1, upper=1, number=1, half_angle_symbol=1):
    text = lowercase(lower) + Uppercase(upper) + strNum(number) + half_angle(half_angle_symbol)
    return text


# 把所有不常用类型的字符拼接在了一起，默认都取一个字符
def ob_text(chi=1, japen=1, arabic=1, fullSymbol=1, Emoji=1):
    text = chinese(chi) + japanese(japen) + Arabic(arabic) + full_symbol(fullSymbol) + emoji(Emoji)
    return text


# 把所有常用和不常用类型的字符拼接在了一起，默认都取一个字符
def al_text(lower=1, upper=1, number=1, half_angle_symbol=1, chi=1, japen=1, arabic=1, fullSymbol=1, Emoji=1):
    text = usu_text(lower=lower, upper=upper, number=number, half_angle_symbol=half_angle_symbol) + ob_text(chi=chi,
                                                                                                            japen=japen,
                                                                                                            arabic=arabic,
                                                                                                            fullSymbol=fullSymbol,
                                                                                                            Emoji=Emoji)
    return text


# info 多少长度的文本  带空格
def _info(num):
    info = ''
    for i in range(int(num / 5)):
        info = info + '%s ' % (f.pystr(min_chars=4, max_chars=4))
    return info


# get now time
def now_time():
    curTime = arrow.now()
    t = curTime.format('YYYY-MM-DD hh:mm:ss')
    return t


# get now timestamp
def now_timestamp():
    curTime = arrow.now()
    t = curTime.timestamp * 1000
    return t


# get sys time
def get_system_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


# get anytime format
def getFormatTime(type='days', num=0, format='YYYY-MM-DD HH:mm:ss', tzinfo=None):
    if not num:
        num = random.randrange(10000)
    t = arrow.now()
    # t = curTime.to(tz=timezone)
    if type == 'days':
        return t.shift(days=-num).format(format)
    if type == 'weeks':
        return t.shift(weeks=num).format(format)
    if type == 'months':
        return t.shift(months=num).format(format)
    if type == 'years':
        return t.shift(years=num).format(format)


# get 当前天的间隔time
def getTimestamp(type='days', num=0, hour=00, minute=00, second=00):
    if type == 'days':
        return arrow.now().shift(days=num).replace(hour=hour, minute=minute, second=second).timestamp * 1000
    if type == 'weeks':
        return arrow.now().shift(weeks=num).replace(hour=hour, minute=minute, second=second).timestamp * 1000
    if type == 'months':
        return arrow.now().shift(months=num).replace(hour=hour, minute=minute, second=second).timestamp * 1000
    if type == 'years':
        return arrow.now().shift(years=num).replace(hour=hour, minute=minute, second=second).timestamp * 1000
    else:
        print('no value,please check void')


# 自定义时间
def getAnyTimestamp(year, month, day, hour=00, minute=00, second=00, tzinfo='+08.00'):
    return arrow.Arrow(year=year, month=month, day=day, hour=hour, minute=minute, second=second,
                       tzinfo=tzinfo).timestamp * 1000


# email
def email():
    email = f.free_email()
    return email


# error_email():
def error_email():
    return ['', ' ', '.1@1.1.1', '123.2123-1@1.1', '1+1.1@1.1', '1@1.1.', 5]


# phone
def phone():
    return f.phone_number()


# 固话
def tel_number():
    numbers = f.phone_number()
    return f"0{numbers[0:3]}-{numbers[3:]}"


# 身份证号
def identity_number():
    return f.ssn(min_age=18, max_age=90)


# 街道信息
def street_address():
    return f.street_address()


# 生成随机经纬度 list
def address_latlng():
    return [int(i) for i in f.latlng()]


# Chrome user-agent info
def ChromeUserAgent():
    return f.chrome()


# error phone
def error_phone():
    return ['', ' ', '@#$%^&!@', '0', '11000000000', '1999999999']


def invalid_email():
    return ['', '    ', '.1@1.1.1', '123.2123-1@1.1', '1+1.1@1.1', '1@1.1.', 5]


def getKeys(dir):
    list = []
    for i in dir.keys():
        list.append(i)
    return list


def getValue(dir):
    list = []
    for i in dir.values():
        list.append(i)
    return list


# 返回值为set 和 None
def checkKeys(pre, dir):
    res = set(dir.keys())
    if pre <= res:
        pass
    else:
        dif = pre - res
        return dif


def _string(n1, n2):
    str = f.pystr(min_chars=n1, max_chars=n2)
    return str


def ipv4():
    ip = f.ipv4()
    return ip


def user_agent():
    ua = f.user_agent()
    return ua


# 返回值为set 和 None
def checkValue(dir, key, value):
    if dir[key] != value:
        return key
    else:
        pass


# 生成时间戳
def timestr():
    start = (2000, 1, 1, 0, 0, 0, 0, 0, 0)
    end = (2020, 1, 1, 0, 0, 0, 0, 0, 0)
    begin = int(time.mktime(start))
    endless = int(time.mktime(end))
    return random.randint(begin, endless)


# 固定值拆分
def fixSum(len, sum):
    if isinstance(sum, str):
        sum = int(sum)
    l = []
    for i in range(len):
        if i != len - 1:
            i = random.randrange(0, sum)
            sum = sum - i
            l.append(i)
        else:
            i = sum
            l.append(i)
    return l


# 将列表拆分为n个子列表
def fixchoose(num, l_choose):
    l = []
    for i in range(num):
        if i != num - 1:
            l1 = random.sample(l_choose, k=random.randrange(0, len(l_choose)))
            l.append(l1)
            l_choose = [i for i in l_choose if i not in l1]
    l.append(l_choose)
    return l


# 时分计算
def hm_time():
    hour = random.randrange(0, 25) * 3600
    minu = random.randrange(0, 60) * 60
    tt = hour + minu
    return tt


# 随机获取一段时间内某一时间的时间戳
def strTimeProp(start='1971-01-01', end='2050-12-31', prop=random.random(), frmt='%Y-%m-%d'):
    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))
    ptime = stime + prop * (etime - stime)
    return int(ptime)


def params_list_to_dict(list):
    d = {}
    for i in list:
        d[i] = i
    return d


def range_int(range):
    min, max = range[0], range[1]
    if not min:
        min = 0
    if not max:
        max = random.randint(int(min), 100)
    return random.randint(int(min), int(max))


def generate_group_level(deep=4):
    level_list = []
    for i in range(deep):
        level_list.append({"title": f"层级{i + 1}", "level": i})
    return level_list


def generate_group_organization(deep=0, level1=0, level2=0, level3=0, level4=0, basecode="code0"):
    group_list = []
    root_node = {"code": basecode, "adminName": f"name0", "title": f"org0", "parentCode": "",
                 "is_root": True}
    group_list.append(root_node)
    if deep > 1:
        for i in range(level1):
            level1_node = {"code": f"{basecode}_{i}", "adminName": f"name0_{i}", "title": f"{basecode}_{i}",
                           "parentCode": f"{basecode}",
                           "is_root": False}
            group_list.append(level1_node)
            if deep > 2:
                for j in range(level2):
                    level2_node = {"code": f"{basecode}_{i}_{j}", "adminName": f"name0_{i}_{j}", "title": f"{basecode}_{i}_{j}",
                                   "parentCode": f"{basecode}_{i}",
                                   "is_root": False}
                    group_list.append(level2_node)
                    if deep > 3:
                        for k in range(level3):
                            level3_node = {"code": f"{basecode}_{i}_{j}_{k}", "adminName": f"name0_{i}_{j}_{k}",
                                           "title": f"{basecode}_{i}_{j}_{k}",
                                           "parentCode": f"{basecode}_{i}_{j}",
                                           "is_root": False}
                            group_list.append(level3_node)
                            if deep > 4:
                                for m in range(level4):
                                    level4_node = {"code": f"{basecode}_{i}_{j}_{k}_{m}",
                                                   "adminName": f"name0_{i}_{j}_{k}_{m}",
                                                   "title": f"{basecode}_{i}_{j}_{k}_{m}",
                                                   "parentCode": f"{basecode}_{i}_{j}_{k}",
                                                   "is_root": False}
                                    group_list.append(level4_node)
    return group_list


if __name__ == '__main__':
    print(generate_group_organization(3, 2, 2))
    # for i in range(2):
    #     print(getFormatTime())
    # # print(getFormatTime())
    # print(f.date(pattern='%Y-%m-%d'))
    # list = ["org_id", "survey_id", "uid", "status", "start_udt", "end_udt", "page", "rowsPerPage"]
    # # print(params_list_to_dict(list))
    # print(range_int([10, 20]))
    # print(getFormatTime(format='yyyy-MM-DD'))
    # item = {"type": "number"}
    # print(type_choose("lang_ch", ['1', '10']))
    # print(type_choose("date", "yyyy-MM-dd"))
    # print(type_choose("number", ['1.2', '1.8', '1']))
