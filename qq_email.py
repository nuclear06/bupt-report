import smtplib
from email.mime.text import MIMEText
from parameter import port


def get_mail(msg_from, msg_to, flag, content, flag2=True):
    if flag2:
        if flag:
            subject = "晨午晚检自动打卡成功"  # 主题
            cont = "晨午晚检打卡成功,填报的信息为：\n{}".format(content)  # 正文
        else:
            subject = "ERROR:晨午晚检打卡出现错误"  # 主题
            cont = "晨午晚检打卡失败，错误信息：\n{}".format(content)  # 正文
    else:
        if flag:
            subject = "每日上报自动打卡成功"  # 主题
            cont = "每日上报打卡成功,填报的信息为：\n{}".format(content)  # 正文
        else:
            subject = "ERROR:每日上报出现错误"  # 主题
            cont = "每日上报出现错误，错误信息：\n{}".format(content)  # 正文
    msg = MIMEText(cont)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    return msg


def right_mail(user, flag2=True, content: str = '-NONE-'):
    if user['mail']:
        s = smtplib.SMTP_SSL('smtp.qq.com', port)  # 邮件服务器及端口号
        try:
            msg_from = user["mail_from"]  # 发送方邮箱
            passwd = user["mail_key"]  # 填入发送方邮箱的授权码
            msg_to = user["mail_to"]  # 收件人邮箱
            msg = get_mail(msg_from, msg_to, True, content, flag2)
            s.login(msg_from, passwd)
            s.sendmail(msg_from, msg_to, msg.as_string())
            print("发送成功")
        except smtplib.SMTPException:
            print("发送失败")
        finally:
            s.quit()
    else:
        print('用户已禁止发送邮件')


def error_mail(user, content: str, flag2=True):
    if user['mail']:
        s = smtplib.SMTP_SSL('smtp.qq.com', port)  # 邮件服务器及端口号
        try:
            msg_from = user["mail_from"]  # 发送方邮箱
            passwd = user["mail_key"]  # 填入发送方邮箱的授权码
            msg_to = user["mail_to"]  # 收件人邮箱
            msg = get_mail(msg_from, msg_to, False, content, flag2)
            s.login(msg_from, passwd)
            s.sendmail(msg_from, msg_to, msg.as_string())
            print("发送成功")
        except smtplib.SMTPException:
            print("发送失败")
        finally:
            s.quit()
    else:
        print('用户已禁止发送邮件')