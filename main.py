import requests
from data import Data
from checks import *
import json
import time
from parameter import *
from qq_email import error_mail
from qq_email import right_mail


def load_user():
    """
    :return:返回用户数据
    """
    user_list = os.environ['USERS']
    return user_list



def main(user):
    flag = 0
    session = requests.Session()
    account = user['user']
    pswd = user['pswd']
    id = user['id']
    while True:
        try:

            flag += 1
            resp1 = session.post(check_url, headers=head, data=Data.get_logindata(account, pswd))
            # 登陆
            message = re_message.search(resp1.text).groups()[0]
            message_check(message)
            # 检测登陆信息


            get_data = Data.get_history(session)
            # 获得历史填报数据
            # print(get_data)
            # return
            ####################################### resp2 = session.post(post_url, headers=head, data=get_data)
            # 填报数据

            if resp1.status_code != 200 and LOGGING:
                main_logger.warning('用户[{}]登陆失败，状态码不是200'.format(id))
            # if resp2.status_code != 200 and LOGGING:
            #     main_logger.warning('用户[{}]填报失败，状态码不是200'.format(id))
            if flag >= MAX_NUM and LOGGING:
                main_logger.error('填报失败次数过多，已终止')
                error_mail(user, '填报失败次数过多，已终止')
                raise Exception('失败次数过多')

        except json.decoder.JSONDecodeError:
            if LOGGING:
                main_logger.error('用户[{}]历史数据获取失败'.format(id))
        except RuntimeWarning as mes:
            print(mes)
            exit(-1)
        #     登陆时会出现的错误
        #     随便找了两个错误来捕捉
        time.sleep(15)

    session.close()


if __name__ == '__main__':
    for i in load_user():
        try:
            main(i)
            right_mail(i)


        except Exception as e:
            print(e)
            other_logger.error('未知错误')
    # if True:
    # print('hello')

    try:
        if LOGGING:
            log_check()
    #         检测日志大小（预设最大10kb）
    except NameError:
        # 未检测到日志文件
        other_logger.warning('未检测到日志文件')
        pass
