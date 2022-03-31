from parameter import post_url
from parameter import re_message
from parameter import backup_checkre
from parameter import other_logger


def message_check(message):
    if message == '操作成功':
        return False
    elif message == "call_user_func() expects parameter 1 to be a valid callback, function '/a_bupt/api/sso/cas' not found or invalid function name":
        return True
    else:
        raise RuntimeWarning(message)


def report_check(session):
    resp = session.post(post_url)
    # print(resp.text)
    message = re_message.search(resp.text).groups()[0]
    if message == '您已上报过':
        other_logger.info('检测填报成功')
        return False
    elif message == '操作成功':
        other_logger.warning('检测填报失败，但是由于检测也算填报，故填报成功')
        return False
    else:
        other_logger.error('填报失败\n'+message)
        return True


def backup_check(text):
    if backup_checkre.search(text):
        raise RuntimeWarning('第二登录方式登录失败！！')
