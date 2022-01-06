#!/usr/bin/env python
# -*- coding: utf-8 -*-
import api.utils.method as md

"""
时间类型数据
"""


class Data:
    # 当前日期 "YYYY-MM-DD"
    now_date = md.getFormatTime()
    # 昨天
    yesterday = md.getFormatTime(num=-1)
    # 一年前
    year_ago = md.getFormatTime(type="years", num=-1)
    # 明天
    tomorrow = md.getFormatTime(type="days", num=1)
    # 一年后
    year_later = md.getFormatTime(type="years", num=1)
    # 时间戳 当前
    now_timestamp = md.now_timestamp()
    # 时间戳 昨天
    yesterday_timestamp = md.getTimestamp(num=-1)
    # 时间戳 一年前
    year_ago_timestamp = md.getTimestamp(type="years", num=-1)
    # 时间戳 一年后later
    year_ago_later = md.getTimestamp(type="years", num=1)
    # 编号
    TimeNo = 'Test' + '_' + md.getFormatTime(format='YYMMDDHHmmss')
    # 标题
    title = '测试' + 'test' + md.strNum(3)
    # 错误编号
    F_No = md.numberTitle()
