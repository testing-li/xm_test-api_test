from api.core.utils import request
import requests

js_url = "https://rs0.bestcem.cn/test/rs/survey/project/61273677ebff9c544df0d2f9/project.js"
source = 2
# try:
data = request.get(url=js_url, env='', headers={"content_type":"application/javascript"})
print(data.history)
#     data.raise_for_status()
# except requests.RequestException as e:
#     print(e)
# else:
#     print(data.headers)
#     print(data.json())
data2 = requests.get(js_url, params={"source": source}, verify=False)
print(data2.content)
# print(data2.url)
# print(data2.content)
