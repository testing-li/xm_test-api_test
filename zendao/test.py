# -*- coding: utf-8 -*-
from api.core.utils import request
import requests
import urllib3
import hashlib
import re

# 通过session的方式进行请求
user = 'xx.zong'
password = 'Zxx1234'
url = 'https://zentao.idiaoyan.cn/user-login.html'

