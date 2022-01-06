#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from api.core.utils import request
from api.utils import method
import random
import re

base = {}
version = ''
structure_list = []
"""
分页和分组的问卷答题时不一样的
"""


def re_short_url(url):
    """
    处理短链接
    :param url: 短链接
    :return: {location,baseurl,qnID,params}
    """
    global base
    base = {}
    r = request.get(url, env='')
    header = r.url
    match_obj = re.match(r'(http.*)/.*/(.*)\?(.*)', re.sub(r"signature", "sig", header), re.M | re.I)
    base['location'] = header
    base['baseurl'] = match_obj.group(1)
    base['qnID'] = match_obj.group(2)
    all_params = {}
    for i in match_obj.group(3).split('&'):
        line = i.split('=')
        all_params[line[0]] = line[1]
    base['allParams'] = all_params
    return base


def base_info(url):
    """
    长链接信息解析
    :param url: 答题链接
    :return: {version, structure_list}
    """
    d = {}
    re_shot = re_short_url(url)
    source = re_shot['allParams']['source']
    baseurl = re_shot['baseurl']
    url = '{}/rs/survey/project/{}/project.js?source={}'.format(baseurl, re_shot['qnID'], source)
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
    d['structure_list'] = structure_list
    global version
    version = data['data']['version']
    d['version'] = version
    return d


def gen_gidmap(structure):
    print(structure)
    gid_map = {}
    cid_map = {}
    gid_map["single"] = {}
    gid_map["multiple"] = {}
    cid_map["single"] = {}
    cid_map["multiple"] = {}
    if len(structure) == 0:
        return {gid_map, cid_map}
    for i in range(len(structure)):
        qtype = structure[i]['qtype']
        if qtype == 'single':  # 单选题
            if not structure[i].get('items'):
                continue
            q_cid = structure[i]['cid']
            q_gid = str(structure[i]['gid'])
            gid_map["single"][q_gid] = {}
            cid_map["single"][q_cid] = {}
            for i in structure[i].get('items'):
                o_gid = str(i["gid"])
                o_oid = str(i["oid"])
                if i.get("is_open"):
                    gid_map["single"][q_gid].setdefault(o_gid, [])
                    cid_map["single"][q_cid].setdefault(o_oid, [])
                else:
                    gid_map["single"][q_gid].setdefault(o_gid, 0)
                    cid_map["single"][q_cid].setdefault(o_oid, 0)
        elif qtype == 'multiple':  # 多选题
            if not structure[i].get('items'):
                continue
            q_cid = structure[i]['cid']
            q_gid = str(structure[i]['gid'])
            gid_map["multiple"][q_gid] = {}
            cid_map["multiple"][q_cid] = {}
            for i in structure[i].get('items'):
                o_gid = i["gid"]
                o_oid = str(i["oid"])
                if i.get("is_open"):
                    gid_map["multiple"][q_gid].setdefault(o_gid, [])
                    cid_map["multiple"][q_cid].setdefault(o_oid, [])
                else:
                    gid_map["multiple"][q_gid].setdefault(o_gid, 0)
                    cid_map["multiple"][q_cid].setdefault(o_oid, [])
    return gid_map, cid_map


d = base_info("https://bestcem.com/t/55YQ26")
q = d["structure_list"]
print(gen_gidmap(q))
