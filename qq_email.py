#from parameter import email_logger
import smtplib
from email.mime.text import MIMEText

s = smtplib.SMTP_SSL('smtp.qq.com', 465)  # 邮件服务器及端口号


def get_mail(msg_from,msg_to,flag,content):

    if flag:
        subject = "晨午晚检自动打卡成功"  # 主题
        cont = "打卡成功,日志信息：\n{}".format(content)  # 正文
    else:
        subject = "ERROR:晨午晚检打卡出现错误"  # 主题
        cont = "错误信息：\n{}".format(content)  # 正文
    msg = MIMEText(cont)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    return msg


def right_mail(user,content='-UNKNOWN-'):
    try:
        msg_from = user["mail_from"]  # 发送方邮箱
        passwd = user["mail_key"]  # 填入发送方邮箱的授权码
        msg_to = user["mail_to"]  # 收件人邮箱
        msg = get_mail(msg_from,msg_to,True,content)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
    except smtplib.SMTPException:
        print("发送失败")
    finally:
        s.quit()


def error_mail(user, content):
    try:
        msg_from = user["mail_from"]  # 发送方邮箱
        passwd = user["mail_key"]  # 填入发送方邮箱的授权码
        msg_to = user["mail_to"]  # 收件人邮箱
        msg = get_mail(msg_from, msg_to, False, content)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
    except smtplib.SMTPException:
        print("发送失败")
        email_logger.info('邮件发送失败')
    finally:
        s.quit()
