# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

# 使用email模块
from email.utils import formataddr


def sentMail(receivers: list, smtp_address, smtp_password, smtp_server, smtp_port, subject, send_from="test report",
             file=None, file_name='', text=None, textType='plain', ssl=False):
    """
    发送邮件
    :param receivers: list 收件人邮箱地址
    :param smtp_address: 发件人邮箱
    :param smtp_password: 发件人邮箱密码
    :param smtp_server: 邮件发送服务的sever地址
    :param smtp_port: 服务端口号
    :param subject: 邮件主题
    :param send_from: 发件人
    :param file: 是否包含附件，传附件地址
    :param file_name: 附件的命名，注意附件类型，name.xlsx excel文件 name.html html文件
    :param text: 邮件的正文部分内容
    :param textType: 正文内容的格式编码，文本用plain，html用html
    :param ssl: 是否开启ssl False不开启
    :return:
    """
    msg = MIMEMultipart()
    sender = smtp_address
    receivers = receivers
    # 创建一个带附件的实例
    msg['From'] = formataddr((f"{send_from}", sender))
    msg['To'] = ','.join(receivers)
    msg['Subject'] = subject
    # 添加正文和附件
    if file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={file_name}')
        msg.attach(part)
    if text:
        msg.attach(MIMEText(text, textType, 'utf-8'))
    # 发送邮件,判断否是通过ssl发送
    try:
        if not ssl:
            server = smtplib.SMTP(smtp_server, smtp_port)
        else:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.set_debuglevel(0)
        server.login(smtp_address, smtp_password)
        server.sendmail(sender, receivers, msg.as_string())
        server.quit()
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
    print(u'Mail sent successfully')
