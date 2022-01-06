# webUI
webUI
Python环境
官方地址下载python安装包 : https://www.python.org/ 1
Python安装文档（windows系统）：https://testing-studio.com/t/topic/57/4 3

官方地址下载pycharm安装包
 JetBrains 4

Download PyCharm: Python IDE for Professional Developers by JetBrains 4
Download the latest version of PyCharm for Windows, macOS or Linux.

安装包
pip install 包名==版本号
pip install selenium==2.39.0
pip install -i 镜像地址 --trusted-host 镜像地址对应的host
举例：pip3 install jupyter -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
国内的pip源
阿里云：https://mirrors.aliyun.com/pypi/simple/
清华：https://pypi.tuna.tsinghua.edu.cn/simple
豆瓣：http://pypi.douban.com/simple/

2，基础的数据类型
Python官方参考文档
https://docs.python.org/3/tutorial/index.html 4

allure：https://demo.qameta.io/allure/# 6

windows/mac通用安装方法
https://github.com/allure-framework/allure2/releases 3 下载allure2.7.zip包,
解压->进入bin目录->运行allure.bat，
把bin目录加入PATH环境变量
Mac 可以使用brew安装:
brew install allure
官网:http://allure.qatools.ru/ 2
文档：https://docs.qameta.io/allure/# 3

生成报告
安装allure-pytest插件
pip install allure-pytest
运行：
在测试执行期间收集结果
pytest [测试文件] -s –q --alluredir=./result/ (—alluredir这个选项 用于指定存储测试结果的路径)
查看测试报告
方式一：测试完成后查看实际报告， 在线看报告，会直接打开默认浏览器展示当前报告
allure serve ./result/ (注意这里的serve书写)
方式二：从结果生成报告，这是一个启动tomcat的服务，需要两个步骤：生成报告，打开报告
生成报告
allure generate ./result/ -o ./report/ --clean (注意：覆盖路径加–clean )
打开报告
allure open -h 127.0.0.1 -p 8883 ./report/

allure运行不同的测试用例
按features运⾏行行测试你⽤用例例
pytest --alluredir= log/report/xml --allure_features=测试登录功能,测试我的自选 testcases/alluredemo
按story运⾏测试⽤例
pytest --alluredir= log/report/xml --allure_stories=测试已登录的场景 testcases/alluredemo
按severity运⾏测试⽤例
pytest --alluredir= log/testreport/xml --allure_severities=blocker testcases/alluredemo
------------------------------------------------------------------------------------------------------------------------
使用：
脚本执行：
pytest tests\test_official\test_account_login.py -s -q --alluredir=.\report\ui_report\result1
allure打开报告
allure serve ./report\ui_report\result1

