# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


# 使用email模块
def sentMail(receivers, stmp_address, smtp_password, smtp_server, smtp_port, file=None, text=None, textType='plain',
             ssl=False):
    msg = MIMEMultipart()
    sender = stmp_address
    receivers = receivers
    # 创建一个带附件的实例
    msg['From'] = Header('tester', 'utf-8')
    msg['To'] = ','.join(receivers)
    msg['Subject'] = 'Auto Testing Report'
    # 添加正文和附件
    if file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="test_report.html"')
        msg.attach(part)
    if text:
        msg.attach(MIMEText(text, textType, 'utf-8'))
    # 发送邮件
    try:
        if not ssl:
            server = smtplib.SMTP(smtp_server, smtp_port)
        else:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.set_debuglevel(1)
        server.login(stmp_address, smtp_password)
        server.sendmail(sender, receivers, msg.as_string())
        server.quit()
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
    print(u'Mail sent successfully')


def sendReport(flag, receivers, stmp_address, smtp_password, smtp_server, smtp_port, file=None, text=None,
               textType='plain'):
    if flag == 'true':
        sentMail(receivers, stmp_address, smtp_password, smtp_server, smtp_port, file, text, textType)
    # lists = os.listdir(resultPath)
    # # 找到最新的测试报告
    # lists.sort(key=lambda fn: os.path.getmtime(resultPath + fn) if not os.path.isdir(resultPath + fn) else 0)
    # # 找到最新的文件
    # newFile = os.path.join(resultPath, lists[-1])
    # # print(newFile)
    # # 调用发邮件模块
    else:
        print('send email functional is off')
