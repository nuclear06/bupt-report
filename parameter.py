import re
import logging

CHECK = True
# 是否允许对是否填报成功进行检测
port = 465
# 邮箱端口，默认为qq邮箱的
DATA_RETURN = True
# 正确填报时是否返回具体填报数据
LOGGING = True
# 是否记录日志（用于填报失败返回数据）
MAX_NUM = 3
# 重复尝试次数最大值

DEBUG = True

backup_checkre = re.compile('手机验证码登录', re.S)
re_message = re.compile('"m":"(.*?)"', re.S)
find = re.compile("(sfzx:.*?askforleave: 0)", re.S)

logging.basicConfig(filename='Running_log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - [line:%(lineno)d] ')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s - [line:%(lineno)d]')
console.setFormatter(formatter)

main_logger = logging.getLogger('main')
other_logger = logging.getLogger('__main__')
email_logger = logging.getLogger('email')

if DEBUG:
    logging.getLogger('check').addHandler(console)
    logging.getLogger('main').addHandler(console)
    logging.getLogger('__main__').addHandler(console)

login_url = 'https://app.bupt.edu.cn/uc/wap/login/check'
backup_login_url = 'https://auth.bupt.edu.cn/authserver/login'

report_url = 'https://app.bupt.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.bupt.edu.cn%2Fsite%2Fncov%2Fxisudailyup'
post_url = 'https://app.bupt.edu.cn/xisuncov/wap/open-report/save'
history_url = 'https://app.bupt.edu.cn/xisuncov/wap/open-report/index'
