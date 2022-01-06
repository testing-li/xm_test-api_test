# -*- coding: utf-8 -*-

import json
from flask import Flask
from flask import request
from api.core.utils import sign_utils
import urllib.parse

app = Flask(__name__)
"""
ngrok 内网穿透
windows
到ngrok目录下执行 ngrok.exe http 5000
将地址返回 填写到回调地址和验证签名的url种

"""


@app.route("/openplatform/survey_submit", methods=['POST'])
def survey_submit():
    data = {}
    call_data = request.json
    data["data"] = call_data
    headers = dict(request.headers)
    paload = json.dumps(call_data)
    # 验证签名
    sign_params = {
        "method": "POST",
        "url": "http://276a-116-232-54-20.ngrok.io/openplatform/survey_submit",
        "body": paload,
    }
    sign = sign_utils.gen_sign(sign_params)
    print(paload)
    print(f"sign is {sign}")
    data["headers"] = headers
    print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False))
    return {"code": 0,
            "msg": "success"}


if __name__ == "__main__":
    app.run("0.0.0.0")
