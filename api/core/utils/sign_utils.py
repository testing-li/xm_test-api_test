# -*- coding: utf-8 -*-
import hashlib
import re
import urllib.parse


def _gen_sign_str(data):
    """
    将任意类型转换为字符串用于签名
    """
    if isinstance(data, dict):
        return gen_sign(data)
    elif isinstance(data, list):
        return ''.join((_gen_sign_str(v) for v in data))
    elif isinstance(data, bool) and not data:
        return ''
    else:
        return str(data)


def md5(a_string):
    """
    生成MD5
    :param a_string:
    :return:
    """
    if not isinstance(a_string, (bytes, str)):
        pass
    if isinstance(a_string, str):
        a_string = a_string.encode('utf-8')
    return hashlib.md5(a_string).hexdigest()


def gen_sign(data):
    params = []
    for k in sorted(data.keys()):
        params.append(k)
        v = data[k]
        if isinstance(v, dict):
            params.append(gen_sign(v))
        elif isinstance(v, list):
            params.append(''.join((_gen_sign_str(_v) for _v in v)))
        elif isinstance(v, bool) and not v:
            # False和'False'相同，但bool值不同，因此False需要作为空串参与签名
            params.append('')
        else:
            params.append(str(v))
    params.append('')
    return md5('|'.join(params))


def get_params(link, third_params: dict):
    matchObj = re.match(r'(.*)\?(.*)', link, re.M | re.I)
    link = matchObj.group(1)
    params = {}
    for i in matchObj.group(2).split('&'):
        l = i.split('=')
        params[l[0]] = l[1]
    for k, v in third_params.items():
        params[k] = v
    params.pop('sign')
    print(params)
    return params, link


def regen_params(link, third_params):
    if 'sign' in link:
        params, link = get_params(link, third_params)
        sign = gen_sign(params)
        params['sign'] = sign
        url = ''.join([link, '?', urllib.parse.urlencode(params)])
    else:
        url = link
    return url


if __name__ == '__main__':
    params = {
        "uuid": "0002",
        "org_code": "xxx",
        "nonce": "1618233149767",
        "code": "AUTO_8",
        "deliver_id": "60751488f9f4f6001d2cd274"
    }
    sign = gen_sign(params)
    print(sign)
    # s1 = 'https://xm-test.bestcem.com/api/open/v1/survey/third/60ab6ba4f9f4f6001e1421ac?bool1=&code=&deliver_id=60ab6ba4f9f4f6001e1421df&int1=&nonce=&org_code=autoopen&sign=&str1='
    # params = {'int1': 1, "str1": 'test', "bool1": 'false'}
    # s2 = regen_params(s1, params)
    # print(s2)
    # print(unquote(s))
    # regen_params(
    #     'https://xm-test.bestcem.com/api/open/v1/survey/third/60ab6ba4f9f4f6001e1421ac?code=&deliver_id=60ab6ba4f9f4f6001e1421df&nonce=&org_code=autoopen&sign=&test1=',
    #     '123')
    # params = {
    #     "uuid": "0002",
    #     "org_code": "xxx",
    #     "nonce": "1618233149767",
    #     "code": "AUTO_8",
    #     "deliver_id": "60751488f9f4f6001d2cd274"
    # }
    # sign = gen_sign(params)
    # print(sign)
