import re
import logging

DATA_RETURN = True
#正确填报时是否返回具体填报数据
LOGGING = True
#是否记录日志（用于填报失败返回数据）
MAX_NUM = 3
# 重复尝试次数最大值


re_message = re.compile('"m":"(.*?)"', re.S)
find = re.compile('(?P<key>.*?): (?P<value>.*)')


logging.basicConfig(filename='Running_log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - [line:%(lineno)d] ')
# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s - [line:%(lineno)d]')
# console.setFormatter(formatter)
main_logger = logging.getLogger('main')
other_logger = logging.getLogger('__main__')
email_logger = logging.getLogger('email')
# logging.getLogger('check').addHandler(console)
# logging.getLogger('main').addHandler(console)
# logging.getLogger('__main__').addHandler(console)

check_url = 'https://app.bupt.edu.cn/uc/wap/login/check'
login_url = 'https://app.bupt.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.bupt.edu.cn%2Fsite%2Fncov%2Fxisudailyup'
post_url = 'https://app.bupt.edu.cn/xisuncov/wap/open-report/save'
history_url = 'https://app.bupt.edu.cn/xisuncov/wap/open-report/index'

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}
