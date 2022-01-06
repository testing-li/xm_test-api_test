# -*- coding: utf-8 -*-
from zendao import zendao_client
from zendao import email_utils
from zendao import generate_data
from datetime import datetime

"""
send to : list  收件人邮箱，用","分隔离
smtp 相关为邮箱的基本配置，根据自己的个人邮箱修改
main为主函数，可以定义一个周期时间范围，开发人员姓名，bug有效范围，和禅道项目的id
"""

send_to = ['xx.zong@idiaoyan.com', "zongxiuxuan001@163.com"]
smtp_address = 'zongxiuxuan001@163.com'
smtp_password = 'QICNSZXVOHBKSMDL'
smtp_server = 'smtp.163.com'
smtp_port = '25'


def main(date, status='', name='', btype=0, username='xx.zong', password='Zxx1234', productID=22):
    """
    通过时间和状态筛选bug列表，生成html正文和excel附件文件，发送邮件
    :param date: 筛选时间，"$lastWeek","$thisWeek","$lastMonth","$thisMonth"
    :param status: "active","resolved","closed"
    :param name: 查询人员姓名
    :param btype: 查询人员范围 0所有bug  1有效bug
    :param username: 禅道登录用户名
    :param password: 禅道密码
    :param password: 禅道bug项目id 如倍市得通用主页‘https://zentao.idiaoyan.cn/bug-browse-22.html’，项目id就是22
    :return:
    """
    # 登录搜索bug记录
    cli = zendao_client.ZentaoClient("https://zentao.idiaoyan.cn", username, password, productID)
    cli.login()
    if name:
        user_list = cli.get_user_list()
        base_data = cli.search_result(date, status, user_list[name])
    else:
        base_data = cli.search_result(date, status)
    if str(btype) == "1":
        base_data = cli.bug_screen(base_data)
    environment_bugs = cli.bug_environment_classify(base_data)
    dever_bugs_count = cli.bug_dever_count(environment_bugs)
    tester_bugs_count = cli.count_tester_bugs(environment_bugs)
    now = datetime.now()
    if date == '$thisWeek':
        timestr = f'{now.year}年{now.month}月第{int(now.strftime("%W")) - int(datetime(now.year, now.month, 1).strftime("%W")) + 1}周'
    elif date == '$thisMonth':
        timestr = f'{now.year}年{now.month}月'
    elif date == '$lastMonth':
        timestr = f'{now.year}年{int(now.month) - 1}月'
    else:
        timestr = ''
    generate_data.generate_bug_html(dever_bugs_count, tester_bugs_count, timestr, name)
    generate_data.generate_bug_excel(base_data, './bugs_record.xlsx')
    # 发送报告
    text = open("./result.html", 'rb').read()
    file = './bugs_record.xlsx'
    email_utils.sentMail(receivers=send_to,
                         smtp_address=smtp_address,
                         smtp_password=smtp_password,
                         smtp_server=smtp_server,
                         smtp_port=smtp_port,
                         subject='禅道Bug统计',
                         file=file,
                         file_name='Zendao_bug_record.xlsx',
                         text=text,
                         textType='html')


if __name__ == '__main__':
    date=("2021-08-01","2021-09-02")
    main(date=date, name='', btype=0, productID=22)
