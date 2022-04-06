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


def daily(_session):
    for _ in range(20):
        resp = _session.get(history_url)
        # print(resp.text)
        history = re.search(
            re.compile('oldInfo: ({"ismoved".*?"id":\d*}),', re.S), resp.text
        ).group(1)
        history = eval(history)
        resp2 = _session.post(daily_report_api, data=history)
        message = re.search(re.compile('"m":"(.*?)"'), resp2.text).groups()[0]
        time.sleep(10)
        if message == '今天已经填报了' or '操作成功':
            daily_logger.info('每日打卡填报成功')
            break
        elif message == '定位信息不能为空':
            raise RuntimeWarning('服务器返回:定位信息不能为空')
        elif _ == 19:
            raise RuntimeWarning(message + '，已达到最大填报尝试次数上限')
        else:
            raise RuntimeWarning(message + ',未预料到的错误')


def load_user():
    """
    :return:返回用户数据
    """
    user_list = eval(os.environ['USERS'])
    text = str(os.environ['DATA'])
    data_list = []
    find_text = data_refind.findall(text)
    # 匹配所有符合格式的数据
    for i in find_text:
        data_find = re.findall(re.compile("(?P<key>.*?): (?P<value>.*)"), i)
        # 对每个人的数据中的属性进行提取
        data_str = '{'
        for j in data_find:
            if j[0] != 'geo_api_info':
                data_str += '"{}":"{}",'.format(*j)
            else:
                data_str += '"{}":{},'.format(*j)
        new_str = data_str[:-1]
        new_str += '}'
        data_list.append(new_str)

    if not len(find_text):
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
                resp_temp = session.get(backup_login_url, headers=Head.head)
                execution = re.search(re.compile('execution" value="(.*?)"/><input '), resp_temp.text).group(1)

                resp1 = session.post(backup_login_url, headers=Head.head,
                                     data=get_logindata(account, pswd, False, execution))

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
                if report_check(session):
                    break
                else:
                    continue
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
    return session


if __name__ == '__main__':
    user_list, data_list = load_user()
    length = len(user_list)
    if len(user_list) != len(data_list):
        raise KeyError("数据读取发生错误")
    for i in range(length):
        try:
            _session = main(user_list[i], data_list[i])
            if DATA_RETURN:
                right_mail(user_list[i], True, str(data_list[i]))
            else:
                right_mail(user_list[i], True)

        except (KeyError, IndexError) as e:
            print(repr(e))
            print("请检查输入的历史填报数据")
            other_logger.error(repr(e))
            error_mail(user_list[i], get_log())
        except Exception as e:
            print(repr(e))
            other_logger.error(repr(e))
            error_mail(user_list[i], get_log())
        # 晨午晚检部分
        ###############################################################################
        # 每日填报部分（如果不需要可以删除以下部分）

        try:
            daily(_session)
            right_mail(user_list[i], False)
        except RuntimeWarning as e:
            print('每日上报出现问题')
            daily_logger.error(str(e))
            error_mail(user_list[i], get_log(), False)
        except Exception as e:
            daily_logger.error(repr(e))
            error_mail(user_list[i], get_log(), False)
        ###############################################################################
