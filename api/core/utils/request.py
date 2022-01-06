import requests
import urllib3
import logging
from api.utils import log
from api.core.utils import aes_utils
from api.core.utils.api_yaml import _CONFIG

log.Logging()


def set_headers(tokenid=None):
    if tokenid:
        return {
            'authorization': str(tokenid)
        }


# set a new headers
def headers_new(a=None, b=None):
    if a and b:
        return {
            a: b
        }


def request(method, url: str, json=None, params=None, token=None, headers=None, files=None, verify=False, ID=None,
            env='bestcem', aes_key=''):
    """
    发送request请求
    :param method: 请求方式
    :param url: 请求的url
    :param json: 请求体，含body
    :param params: 请求参数，表格参数
    :param token: 鉴权token，jwt
    :param files: 请求文件
    :param verify: 证书验证 默认不验证
    :param ID: url路径含ID
    :param env: 是否读取配置环境
    :return:
    """
    if env:
        id_url = url.format(ID=ID)
        _url = f'{_CONFIG["base_url"][_CONFIG["env"]][env]}{id_url}'
    else:
        _url = url
    if token:
        header = set_headers(token)
    else:
        header = headers
    payload = None
    if json:
        payload = {}
        for k, v in json.items():
            if v != None:
                payload[k] = v
    if params:
        exclude_params = {}
        for k, v in params.items():
            if v is not None:
                exclude_params[k] = v
        params = exclude_params
    try:
        urllib3.disable_warnings()
        response = requests.request(
            method=method,
            url=_url,
            json=payload,
            params=params,
            headers=header,
            files=files,
            verify=verify,
            allow_redirects=True
        )
    except requests.RequestException as e:
        logging.error('RequestException URL : %s' % url)
        logging.error('RequestException Info: %s' % e)
        return

    except Exception as e:
        logging.error('Exception URL : %s' % url)
        logging.error('Exception Info: %s' % e)
        return

    time_total = response.elapsed.total_seconds()
    status_code = response.status_code

    logging.info("-" * 100)
    logging.info('[      api      ] : {}'.format(url))
    logging.info('[  request url  ] : {}'.format(response.url))
    logging.info('[     method    ] : {}'.format(method.upper()))
    logging.info('[request headers] : {}'.format(header))
    if json:
        logging.info(f'[request payload] : {payload}')
    if params:
        logging.info(f'[request params ] : {params}')
    if files:
        logging.info(f'[ request files ] : {files}')
    logging.info('[  status code  ] : {}'.format(status_code))
    logging.info('[   time total  ] : {} s'.format(time_total))
    if "application/json" in response.headers.get("Content-Type"):
        logging.info('[ response json ] : %s' % response.json())
    else:
        logging.info('[ response text ] : %s' % response.content)
    logging.info("-" * 100)
    if aes_key and response.json()['code'] == 0 and 'encrypt' in response.json().keys():
        aes_response = response.json()
        aes_response['data'] = aes_utils.aes_cryption(type='decode', data=aes_response['encrypt'],
                                                      AES_KEY=aes_key)
        if aes_key:
            logging.info(f'[ response aes ] : {aes_response["data"]}')
        return aes_response['data']
    return response


# post
def post(url, payload=None, token=None, headers=None, params=None, file=None, ID=None, env='bestcem', aes_key=''):
    """
    :param url: 请求url地址
    :param payload: 参数类型为json，传{}
    :param token: 是否需要token认证
    :param param: 参数为表单,传{}
    :param file: 上传文件的key值和地址，传(key,path)
    :return: response
    """
    if file:
        if params:
            for k, v in params.items():
                params[k] = (None, str(v))
            params[file[0]] = (file[1].split('/')[-1], open(file[1], 'rb'))
        else:
            file = {file[0]: (file[1].split('/')[-1], open(file[1], 'rb'))}
        return request('POST', url=url, token=token, files=file, headers=headers, ID=ID, env=env, aes_key=aes_key)
    else:
        return request('POST', url=url, json=payload, params=params, token=token, headers=headers, ID=ID, env=env,
                       aes_key=aes_key)


# get
def get(url, params=None, token=None, headers=None, ID=None, env='bestcem', aes_key=''):
    return request('GET', url=url, params=params, token=token, headers=headers, ID=ID, env=env, aes_key=aes_key)


# put
def put(url, payload=None, token=None, headers=None, ID=None, env='bestcem', aes_key=''):
    return request('PUT', url=url, json=payload, headers=headers, token=token, ID=ID, env=env, aes_key=aes_key)


# delete
def delete(url, token=None, payload=None, headers=None, ID=None, env='bestcem', aes_key=''):
    return request('DELETE', url, json=payload, token=token, headers=headers, ID=ID, env=env, aes_key=aes_key)


if __name__ == '__main__':
    print()
