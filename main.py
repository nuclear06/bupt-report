import requests
from requests.adapters import HTTPAdapter
from data import *
from checks import *
import time
from parameter import *
from qq_email import error_mail
from qq_email import right_mail
from resp import *
import os


def load_user():
    """
    :return:返回用户数据
    """
    user_list = eval(os.environ['USERS'])
    text = str(os.environ['DATA'])
    data_list = []
    _iter = find.finditer(text)
    iter_len = 0
    for _ in _iter:
        for j in _.groups():
            iter_len += 1
            data = '{' + j.replace('\n', ' ') + '}'
            data_list.append(data)
    if not iter_len:
        raise RuntimeWarning('正则匹配到的信息为空')

    return user_list, data_list


def main(user, post_data):
    myresp = Resp()
    login_way = 1
    # 记录登陆方式
    flag = 0
    # 记录已重试次数
    RETURN_EMAIL = user['mail']
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=15))
    session.mount('https://', HTTPAdapter(max_retries=15))
    account = user['user']
    pswd = user['pswd']
    myid = user['id']
    while True:
        try:

            flag += 1
            if flag > MAX_NUM:
                error = '[{}]失败次数过多，其填报已终止'.format(myid)
                raise ZeroDivisionError(error)
            if login_way == 1:
                resp1 = session.post(login_url, headers=Head.head, data=get_logindata(account, pswd))
                myresp.add_resp('resp1', resp1)
                # 登陆
                message = re_message.search(resp1.text).groups()[0]
                # 检测登陆信息
                if message_check(message):
                    '''
                    检测登陆信息，如果成功返回False，失败抛出异常，是另外的登录方式自动切换
                    '''
                    login_way = 2
                    continue
            elif login_way == 2:
                main_logger.info('登录方式已切换')
                resp1 = session.post(backup_login_url, headers=Head.backup_head,
                                     data=get_logindata(account, pswd, False))
                backup_check(resp1.text)
                main_logger.info('{}登录成功'.format(myid))
                myresp.add_resp('resp1', resp1)
            try:
                resp2 = session.post(post_url, headers=Head.head, data=post_data.encode('utf-8'))
            # 填报数据
            except Exception as e:
                main_logger.error(repr(e) + '  填报数据时发生错误')
                time.sleep(15)
                continue

            if myresp.resp_dict['resp1'].status_code != 200:
                main_logger.warning('用户[{}]登陆失败，状态码不是200'.format(myid))
                time.sleep(15)
                # 延迟一段时间后重试
                continue
            else:
                main_logger.info('{}登录页面连接成功，状态码为200'.format(myid))

            if resp2.status_code != 200:
                main_logger.warning('用户[{}]填报失败，状态码不是200'.format(myid))
                time.sleep(15)
                # 延迟一段时间后重试
                continue
            else:
                main_logger.info('{}填报页面连接成功，状态码为200'.format(myid))

            if CHECK:
                report_check(session)

            break
        #     正常执行一次结束
        except requests.ConnectionError as er:
            repr(er)
            main_logger.error(str(er))
            time.sleep(15)
            continue
        #     第二登陆方式莫名其妙会出现的问题

        except ZeroDivisionError as mes:
            print(mes)
            main_logger.error(str(mes))
            if RETURN_EMAIL:
                error_mail(user, get_log())
            exit(-1)
            # 登陆失败次数达到最大时会抛出的异常

        except RuntimeWarning as mes:
            print(str(mes) + '请检查输入的账户信息')
            if RETURN_EMAIL:
                error_mail(user, str(mes) + '请检查输入的账户信息')
            exit(-1)
        #     登陆失败时会抛出出现的错误
        #     随便找了两个错误来捕捉
    session.close()


if __name__ == '__main__':
    user_list, data_list = load_user()
    length = len(user_list)
    if len(user_list) != len(data_list):
        raise KeyError("数据读取发生错误")
    for i in range(length):

        try:
            main(user_list[i], data_list[i])
            if user_list[i]['mail']:
                if DATA_RETURN:
                    right_mail(user_list[i], str(data_list[i]))
                else:
                    right_mail(user_list[i])

        except (KeyError, IndexError) as e:
            print(repr(e))
            print("请检查输入的历史填报数据")
            other_logger.error(repr(e))
            if user_list[i]['mail']:
                error_mail(user_list[i], get_log())
        except Exception as e:
            print(repr(e))
            other_logger.error(repr(e))
            if user_list[i]['mail']:
                error_mail(user_list[i], get_log())
