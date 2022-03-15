import logging
from qq_email import error_mail
from qq_email import right_mail

right_mail(USERS[0],)
logging.basicConfig(filename='Running_log', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - [line:%(lineno)d] ')
logger = logging.getLogger('test')
logger.error('test')
logger.info('test')
logger.warning('test')
logger.debug('test')
print('日志记录完毕')
with open('Running_log') as f:
  temp = f.read()
  right_mail(USER,temp)
  
